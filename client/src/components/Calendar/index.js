import React, { Component } from 'react';
import PropTypes from 'prop-types';
// import SelectedDate from './SelectedDate';
import Rooms from './Rooms';
import Hours from './Hours';
import Cells from './Cells';
import Navigation from '../Navigation';
import api from '../../utils/api';
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
  };

  /*
   * COMPONENT LIFE CYCLE
   */

  componentDidMount() {
    document.body.style.backgroundColor = '#3d3d3e';

    this.getBookings();
    this.getRooms();

    // Set up hours
    const hoursSettings = {
      start: '08:00',
      end: '23:00',
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
    this.setState({ hoursSettings, hoursList: hours });

    // Set up variables in scss
    const gridRowNum = minutesIncrement * hours.length / 10;

    document.documentElement.style.setProperty('--rowNum', hours.length);
    document.documentElement.style.setProperty('--cellsDivisionNum', gridRowNum);
  }

  componentWillUnmount() {
    document.body.style.backgroundColor = 'white';
  }

  /*
   * REQUESTS
   */

  // propsTesting* is used for Jest testing
  getBookings() {
    const { propsTestingBookings } = this.props;
    const test = !!propsTestingBookings;
    if (test) {
      this.setState({ bookings: propsTestingBookings });
    } else {
      const { selectedDate } = this.state;
      const params = {
        year: selectedDate.getFullYear(),
        month: selectedDate.getMonth() + 1,
        day: selectedDate.getDate(),
      };

      api.getBookings(params)
        .then((response) => {
          this.setState({ bookings: response.data });
          this.getCampOns(params);
        });
    }
  }

  getCampOns(params) {
    const { propsTestingCampOns } = this.props;
    const test = !!propsTestingCampOns;
    if (test) {
      this.setState({ campOns: propsTestingCampOns });
    } else {
      api.getCampOns(params)
        .then((response) => {
          this.setState({ campOns: response.data }, () => {
          // this.campOnToBooking();
          });
        });
    }
  }

  getRooms() {
    const { propsTestingRooms } = this.props;
    const test = !!propsTestingRooms;
    if (test) {
      this.setState({ roomsList: propsTestingRooms });
    } else {
      api.getRooms()
        .then((response) => {
          this.setState({ roomsList: response.data });
          const colNumber = response.data.length;
          document.documentElement.style.setProperty('--colNum', colNumber);
        });
    }
  }

  /*
   * HELPER METHOD
   */

  changeDate = (date) => {
    this.setState({ selectedDate: date }, () => {
      this.getBookings();
    });
  }

  onCloseModalWithAction = () => {
    this.getBookings();
  }

  campOnToBooking = () => {
    const { bookings, campOns } = this.state;
    const campOnBookings = [];
    if (!!campOns && !!bookings) {
      campOns.forEach((campOn) => {
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
          id: `camp${campOn.camped_on_booking}`,
          isCampOn: true,
        });
      });
      campOnBookings.forEach((campOnBooking) => {
        bookings.push(campOnBooking);
      });
      this.setState({ bookings });
    }
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
    } = this.state;
    return [
      <Navigation
        key={0}
        showDate
        changeDate={this.changeDate}
        onOpenDatePicker={Calendar.onOpenDatePicker}
        onCloseDatePicker={Calendar.onCloseDatePicker}
      />,
      <div className="calendar__container" key={1}>
        <div className="calendar__wrapper">
          <Rooms roomsList={roomsList} changeDate={this.changeDate} />
          <Hours hoursList={hoursList} />
          <Cells
            hoursSettings={hoursSettings}
            bookings={bookings}
            roomsList={roomsList}
            hoursList={hoursList}
            campOns={campOns}
            selectedDate={selectedDate}
            onCloseModalWithAction={this.onCloseModalWithAction}
          />
        </div>
      </div>,
    ];
  }
}

Calendar.propTypes = {
  propsTestingBookings: PropTypes.instanceOf(Object),
  propsTestingCampOns: PropTypes.instanceOf(Object),
  propsTestingRooms: PropTypes.instanceOf(Object),
};

Calendar.defaultProps = {
  propsTestingBookings: null,
  propsTestingCampOns: null,
  propsTestingRooms: null,
};

export default Calendar;
