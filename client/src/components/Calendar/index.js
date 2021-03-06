import React, { Component } from 'react';
import { Icon } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import Announcement from './Announcement';
import Cells from './Cells';
import Header from './Header';
import Navigation from '../Navigation';
import api from '../../utils/api';
import storage from '../../utils/local-storage';
import RoomsSelection from './RoomsSelection';
import './Calendar.scss';

class Calendar extends Component {
  static timeStringToInt(time) {
    const tokens = time.split(':');
    const timeInt = {
      hour: parseInt(tokens[0], 10),
      minutes: parseInt(tokens[1], 10),
    };
    return timeInt;
  }

  static onOpenDatePicker() {
    document.documentElement.style.setProperty('--opacity', 0.2);
    document.documentElement.style.setProperty('--pointerEvents', 'none');
  }

  static onCloseDatePicker() {
    document.documentElement.style.setProperty('--opacity', 1);
    document.documentElement.style.setProperty('--pointerEvents', 'auto');
  }

  state = {
    roomsList: [],
    hoursList: [],
    selectedDate: new Date(),
    roomsNum: 0,
    hoursDivisionNum: 0,
    orientation: 1,
    update: false,
    unavailabilities: [],
    showRoomsSelection: false,
    roomsToDisplay: [],
  };

  /*
   * COMPONENT LIFE CYCLE
   */

  componentDidMount() {
    document.body.style.backgroundColor = '#F2D692';
    this.setState(
      { orientation: storage.getOrientation() === null ? 1 : storage.getOrientation() },
    );
    this.getBookings();
    this.getRooms();
    this.setHours();

    this.interval = setInterval(() => this.refreshPage(), 60000);
  }

  componentWillUnmount() {
    document.body.style.backgroundColor = 'white';
    clearInterval(this.interval);
  }

  /*
   * REQUESTS
   */
  // propsTesting* is used for Jest testing
  getBookings() {
    const { propsTestingBookings, propsTestingCampOns } = this.props;
    const test = !!propsTestingBookings;
    if (test) {
      this.setState({ bookings: propsTestingBookings, campOns: propsTestingCampOns });
    } else {
      const { selectedDate } = this.state;
      const params = {
        year: selectedDate.getFullYear(),
        month: selectedDate.getMonth() + 1,
        day: selectedDate.getDate(),
      };

      Promise.all([api.getBookings(params), api.getCampOns(params)]).then((results) => {
        const bookings = results[0].data;
        const campons = results[1].data;
        this.campOnToBooking(campons, bookings);
      });
    }
  }

  getRooms() {
    const { propsTestingRooms, forDisplay } = this.props;
    const test = !!propsTestingRooms;
    if (test) {
      this.setState({ roomsList: propsTestingRooms });
    } else {
      Promise.all([api.getRooms(), api.getRoomAvailabilities()]).then((results) => {
        if (forDisplay) {
          this.setState({
            roomsList: results[0].data,
            roomsNum: results[0].data.length,
            unavailabilities: results[1].data,
            roomsToDisplay: results[0].data,
          }, () => {
            this.setState({ showRoomsSelection: true });
          });
        } else {
          this.setState({
            roomsList: results[0].data,
            roomsNum: results[0].data.length,
            unavailabilities: results[1].data,
          });
        }
      });
    }
  }

  setHours = () => {
    const hoursSettings = {
      start: '08:00',
      end: '22:00',
      increment: 60,
    };
    const hourStart = Calendar.timeStringToInt(hoursSettings.start);
    const hourEnd = Calendar.timeStringToInt(hoursSettings.end);

    const minutesIncrement = hoursSettings.increment;
    const hours = [];
    const time = new Date();
    time.setHours(hourStart.hour, hourStart.minutes, 0);

    // Format time for display in table
    let currentTime = hourStart.hour * 60 + hourStart.minutes;
    const endTime = hourEnd.hour * 60 + hourEnd.minutes;

    while (currentTime <= endTime) {
      hours.push(time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
      time.setMinutes(time.getMinutes() + minutesIncrement);
      currentTime += minutesIncrement;
    }
    const hoursDivisionNum = minutesIncrement * hours.length / 10;

    this.setState({
      hoursSettings,
      hoursList: hours,
      hoursDivisionNum,
    });
  }

  setStyle() {
    const { orientation } = this.state;
    let style;
    if (orientation === 0) {
      style = {
        wrapper: {
          gridTemplateRows: 'max-content auto',
        },
      };
    } else {
      style = {
        wrapper: {
          gridTemplateColumns: 'max-content auto',
        },
      };
    }
    return style;
  }

  /*
   * HELPER METHOD
   */

  refreshPage = () => {
    const { forDisplay } = this.props;
    const { update } = this.state;
    if (forDisplay) {
      this.setState({
        update: !update,
        selectedDate: new Date(),
      });
    }
    this.getBookings();
  }

  changeDate = (date) => {
    this.setState({ selectedDate: date }, () => {
      this.getBookings();
    });
  }

  changeOrientation = () => {
    const { orientation } = this.state;
    const newOrientation = orientation === 0 ? 1 : 0;
    storage.saveOrientation(newOrientation);
    this.setState({ orientation: newOrientation });
  }

  onCloseModalWithAction = () => {
    this.getBookings();
  }

  closeRoomsSelection = (rooms) => {
    this.setState({ roomsNum: rooms.length, roomsToDisplay: rooms, showRoomsSelection: false });
  }

  campOnToBooking = (campOns, bookings) => {
    const campOnBookings = [];
    if (!!campOns && !!bookings) {
      campOns.forEach((campOn, index) => {
        let dateCampOn = '';
        let roomCampOn = '';
        if (bookings) {
          for (let i = 0; i < bookings.length; i += 1) {
            if (bookings[i].id === campOn.camped_on_booking) {
              const { date, room } = bookings[i];
              dateCampOn = date;
              roomCampOn = room;
              break;
            }
          }
        }
        campOnBookings.push({
          date: dateCampOn,
          start_time: campOn.start_time,
          end_time: campOn.end_time,
          booker: campOn.booker,
          room: roomCampOn,
          id: `camp${campOn.camped_on_booking}-${index}`,
          isCampOn: true,
          camped_on_booking: campOn.camped_on_booking,
          camp_on_id: campOn.id,
        });
      });
      campOnBookings.forEach((campOnBooking) => {
        bookings.push(campOnBooking);
      });
      this.setState({ bookings, campOns });
    }
  }

  update = () => {
    this.getBookings();
    this.setState({ update: true });
    this.setState({ update: false });
  }

  /*
   * COMPONENT RENDERING
   */

  render() {
    const {
      roomsList,
      hoursList,
      hoursSettings,
      bookings,
      campOns,
      selectedDate,
      orientation,
      roomsNum,
      hoursDivisionNum,
      update,
      unavailabilities,
      showRoomsSelection,
      roomsToDisplay,
    } = this.state;
    const { forDisplay } = this.props;
    let colList = forDisplay ? roomsToDisplay : roomsList;
    let colName = 'room';
    let rowList = hoursList;
    let rowName = 'hour';
    if (orientation === 1) {
      rowList = forDisplay ? roomsToDisplay : roomsList;
      rowName = 'room';
      colList = hoursList;
      colName = 'hour';
    }
    return (
      <div className="main__page">
        <Navigation
          key={0}
          showDate
          changeDate={this.changeDate}
          onOpenDatePicker={Calendar.onOpenDatePicker}
          onCloseDatePicker={Calendar.onCloseDatePicker}
          update={update}
          forDisplay={forDisplay}
        />
        {forDisplay
          ? (
            <RoomsSelection
              show={showRoomsSelection}
              rooms={roomsList}
              roomsToDisplay={roomsToDisplay}
              onClose={this.closeRoomsSelection}
            />)
          : null}
        <div className="calendar__container" key={1}>
          <Announcement />
          <div className="calendar__wrapper" style={this.setStyle().wrapper}>
            <button type="button" className="button_orientation" onClick={() => this.changeOrientation()}><Icon name="exchange" /></button>
            <Header headerList={colList} type="column" name={colName} />
            <Header headerList={rowList} type="row" name={rowName} />
            <Cells
              hoursSettings={hoursSettings}
              bookings={bookings}
              roomsList={forDisplay ? roomsToDisplay : roomsList}
              hoursList={hoursList}
              unavailabilities={unavailabilities}
              campOns={campOns}
              selectedDate={selectedDate}
              onCloseModalWithAction={this.onCloseModalWithAction}
              orientation={orientation}
              roomsNum={roomsNum}
              hoursDivisionNum={hoursDivisionNum}
              update={this.update}
            />
          </div>
        </div>
      </div>
    );
  }
}

Calendar.propTypes = {
  propsTestingBookings: PropTypes.instanceOf(Object),
  propsTestingCampOns: PropTypes.instanceOf(Object),
  propsTestingRooms: PropTypes.instanceOf(Object),
  forDisplay: PropTypes.bool,
};

Calendar.defaultProps = {
  propsTestingBookings: null,
  propsTestingCampOns: null,
  propsTestingRooms: null,
  forDisplay: false,
};

export default Calendar;
