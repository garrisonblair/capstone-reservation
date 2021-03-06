import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {
  Label,
  Popup,
  Icon,
  Message,
} from 'semantic-ui-react';
import './Calendar.scss';
import moment from 'moment';
import ReservationDetailsModal from '../ReservationDetailsModal';
import BookingInfoModal from '../BookingInfoModal';
import storage from '../../utils/local-storage';
import api from '../../utils/api';

class Cells extends Component {
  static timeStringToInt(time) {
    const tokens = time.split(':');
    const timeInt = {
      hour: parseInt(tokens[0], 10),
      minutes: parseInt(tokens[1], 10),
    };
    return timeInt;
  }

  state = {
    selectedHour: '',
    selectedRoomName: '',
    selectedRoomId: '',
    selectedRoomCurrentBookings: [],
    selectedBooking: {},
    selectedBookingCampons: null,
    bookingModal: false,
    bookingInfoModal: false,
    hoursDivisionNum: 0,
    roomsNum: 0,
    orientation: 0,
    bookingColor: '#1F5465',
    camponColor: '#82220E',
    passedBookingColor: '#7F7F7F',
  };

  componentDidMount() {
    if (storage.getUser() !== null) {
      this.syncSettings(this.getServiceToken());
    }
  }

  getServiceToken = () => {
    // eslint-disable-next-line react/prop-types
    const { match } = this.props;
    let token;
    if (match !== undefined) {
      // eslint-disable-next-line prefer-destructuring
      token = match.params.token;
    }
    return token;
  }

  static getDerivedStateFromProps(props, state) {
    if (
      props.bookings === state.bookings
      && props.orientation === state.orientation
      && props.roomsNum === state.roomsNum) {
      return null;
    }
    return {
      bookings: props.bookings,
      orientation: props.orientation,
      roomsNum: props.roomsNum,
      hoursDivisionNum: props.hoursDivisionNum,
    };
  }

  static getPopupContent(booking) {
    const start = booking.start_time.length > 5
      ? booking.start_time.substring(0, booking.start_time.length - 3) : booking.start_time;
    const end = booking.end_time.length > 5
      ? booking.end_time.substring(0, booking.end_time.length - 3) : booking.end_time;
    const popup = {
      content:
  <span>
    <Label color="blue">
      {start}
      -
      {end}
    </Label>
    <Label color="yellow">{booking.booker.username}</Label>
    {booking.isCampOn
      ? <Label color="red">CAMPON</Label> : null}
  </span>,
    };
    return popup;
  }
  /*
   * STYLE METHODS
   */

  // Style for .calendar__cells__cell
  setCellStyle(hourRow, unavailability) {
    const { hoursSettings } = this.props;
    const { orientation } = this.state;
    const start = (hourRow * hoursSettings.increment / 10) + 1;
    const end = start + hoursSettings.increment / 10;
    let color = '';
    let event = 'auto';
    if (unavailability) {
      color = 'rgb(127, 127, 127)';
      if (!storage.checkAdmin()) {
        event = 'none';
      }
    }
    // const height = '65px';
    let style;
    if (orientation === 0) {
      style = {
        cell_style: {
          gridRowStart: start,
          gridRowEnd: end,
          gridColumn: 1,
          width: '120px',
          backgroundColor: color,
          pointerEvents: event,
        },
      };
    } else {
      style = {
        cell_style: {
          gridColumnStart: start,
          gridColumnEnd: end,
          gridRow: 1,
          backgroundColor: color,
          pointerEvents: event,
        },
      };
    }
    return style;
  }

  // Style for .calendar__rooms__cells and .calendar__cells__wrapper
  setStyle() {
    const { roomsNum, orientation, hoursDivisionNum } = this.state;
    let style;
    if (orientation === 0) {
      style = {
        wrapper: {
          gridTemplateColumns: `repeat(${roomsNum}, 1fr)`,
        },
        division: {
          gridTemplateRows: `repeat(${hoursDivisionNum}, 1fr)`,
        },
      };
    } else {
      style = {
        wrapper: {
          gridTemplateRows: `repeat(${roomsNum}, 1fr)`,
        },
        division: {
          gridTemplateColumns: `repeat(${hoursDivisionNum}, 1fr)`,
        },
      };
    }
    return style;
  }


  // Style for .calendar__booking
  setBookingStyle(booking) {
    const { hoursSettings } = this.props;
    const {
      orientation,
      bookingColor,
      camponColor,
      passedBookingColor,
    } = this.state;
    const bookingStart = Cells.timeStringToInt(booking.start_time);
    const bookingEnd = Cells.timeStringToInt(booking.end_time);
    const calendarStart = Cells.timeStringToInt(hoursSettings.start);
    let color = bookingColor;
    const currentDate = new Date();
    const currentMinute = currentDate.getMinutes() < 10 ? `0${currentDate.getMinutes()}` : `${currentDate.getMinutes()}`;

    // Change booking color if it's passed
    const bookingDate = booking.date.split('-');
    let datePassed = false;
    let sameDate = false;
    if (parseInt(bookingDate[0], 10) < currentDate.getFullYear()) {
      datePassed = true;
    } else if (parseInt(bookingDate[0], 10) === currentDate.getFullYear()) {
      if (parseInt(bookingDate[1], 10) < currentDate.getMonth() + 1) {
        datePassed = true;
      } else if (parseInt(bookingDate[1], 10) === currentDate.getMonth() + 1) {
        if (parseInt(bookingDate[2], 10) < currentDate.getDate()) {
          datePassed = true;
        } else if (parseInt(bookingDate[2], 10) === currentDate.getDate()) {
          sameDate = true;
        }
      }
    }
    if (datePassed || (sameDate && parseInt(booking.end_time.replace(/:/g, ''), 10) <= parseInt(`${currentDate.getHours()}${currentMinute}00`, 10))) {
      color = passedBookingColor;
    } else
    if (booking.isCampOn) {
      color = camponColor;
    }

    // Find the rows in the grid the booking corresponds to.
    // Assuming an hour is divided in 6 rows, each representing an increment of 10 minutes.
    const start = ((bookingStart.hour * 60 + bookingStart.minutes)
                      - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;
    const end = ((bookingEnd.hour * 60 + bookingEnd.minutes)
                    - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;
    let style;
    if (orientation === 0) {
      style = {
        booking_style: {
          gridRowStart: start,
          gridRowEnd: end,
          gridColumn: 1,
          backgroundColor: color,
          borderLeft: '1px solid white',
          borderTop: '1px solid white',
          borderBottom: '1px solid white',
          width: booking.isCampOn ? '66.1%' : '99.1%',
          transform: booking.isCampOn ? 'translateX(50%)' : '',
        },
      };
    } else {
      style = {
        booking_style: {
          gridColumnStart: start,
          gridColumnEnd: end,
          gridRow: 1,
          backgroundColor: color,
          borderLeft: '1px solid white',
          borderRight: '1px solid white',
          borderTop: '1px solid white',
          height: booking.isCampOn ? '65%' : '98%',
          transform: booking.isCampOn ? 'translateY(50%)' : '',
        },
      };
    }

    return style;
  }

  /*
  * HELPER METHOD
  */

  static getBookingDuration(booking) {
    let hourDiff = booking.end_time.replace(/:/g, '').substring(0, 2) - booking.start_time.replace(/:/g, '').substring(0, 2);
    let minuteDiff = booking.end_time.replace(/:/g, '').substring(2, 4) - booking.start_time.replace(/:/g, '').substring(2, 4);
    if (minuteDiff < 0) {
      minuteDiff += 60;
      hourDiff -= 1;
    }
    return (hourDiff * 100 + minuteDiff);
  }

  getCamponsForBooking(booking) {
    const { campOns } = this.props;
    const campOnsList = [];
    const c = !!campOns;
    if (c) {
      campOns.forEach((campOn) => {
        if (campOn.camped_on_booking === booking.id) {
          campOnsList.push(campOn);
        }
      });
    }
    return campOnsList;
  }

  syncSettings = (token) => {
    api.getPersonalSettings(token)
      .then((r) => {
        if (r.status === 200) {
          this.setState({
            bookingColor: r.data.booking_color,
            camponColor: r.data.campon_color,
            passedBookingColor: r.data.passed_booking_color,
          });
        }
      });
  }

  toggleBookingModal = () => {
    const { bookingModal } = this.state;
    this.setState({ bookingModal: !bookingModal });
    if (bookingModal) {
      this.update();
    }
  }

  toggleBookingInfoModal = () => {
    const { bookingInfoModal } = this.state;
    this.setState({ bookingInfoModal: !bookingInfoModal });
    if (bookingInfoModal) {
      this.update();
    }
  }

  toggleBookingModalWithReservation = () => {
    const { onCloseModalWithAction } = this.props;
    this.setState({ bookingModal: false, bookingInfoModal: false });
    onCloseModalWithAction();
    this.update();
  }

  toggleBookingInfoWithAction = () => {
    const { onCloseModalWithAction } = this.props;
    this.setState({ bookingModal: false, bookingInfoModal: false });
    onCloseModalWithAction();
    this.update();
  }

  /*
   * CLICK HANDLING METHODS
   */

  handleClickCell = (currentHour, currentRoom) => {
    const selectedRoomId = `${currentRoom.id}`;
    const selectedRoomName = currentRoom.name;
    const selectedHour = currentHour;
    const selectedRoomCurrentBookings = [];
    const { bookings } = this.props;
    bookings.forEach((booking) => {
      if (booking.room === selectedRoomId) {
        selectedRoomCurrentBookings.push(booking);
      }
    });
    this.setState({
      selectedHour,
      selectedRoomId,
      selectedRoomName,
      selectedRoomCurrentBookings,
    });
    this.toggleBookingModal();
  }

  handleClickBooking = (booking) => {
    const { roomsList, campOns } = this.props;
    const selectedBookingCampons = [];
    let roomName = '';

    roomsList.forEach((room) => {
      if (room.id === booking.room) {
        roomName = room.name;
        // return;
      }
    });
    if (campOns.length > 0) {
      campOns.forEach((campon) => {
        if (campon.camped_on_booking === booking.id) {
          selectedBookingCampons.push(campon);
        }
      });
    }
    this.setState({
      selectedBooking: booking,
      selectedRoomName: roomName,
      selectedBookingCampons,
    }, () => {
      this.toggleBookingInfoModal();
    });
  }

  update = () => {
    const { update } = this.props;
    update();
  }

  checkAvailability = (unavailabilities, hour) => {
    const { selectedDate } = this.props;
    let currentHour = hour;
    if (unavailabilities.length === 0) { return false; }
    if (currentHour.split(' ').length === 2) {
      currentHour = currentHour.split(' ');
      if (currentHour[1] === 'PM' && currentHour[0].split(':')[0] !== '12') {
        const newHour = currentHour[0].split(':');
        newHour[0] = (parseInt(newHour[0], 10) + 12).toString();
        currentHour = `${newHour[0]}:${newHour[1]}`;
      } else {
        // eslint-disable-next-line prefer-destructuring
        currentHour = currentHour[0];
      }
    }
    for (let i = 0; i < unavailabilities.length; i += 1) {
      const s = unavailabilities[i].start_time.split('T');
      const e = unavailabilities[i].end_time.split('T');
      const startDate = moment(s[0], 'YYYY-MM-DD');
      let startTime = s[1].split('-');
      startTime = startTime[0].split(':');
      startDate.set({ h: startTime[0], m: startTime[1] });
      const endDate = moment(e[0], 'YYYY-MM-DD');
      let endTime = e[1].split('-');
      endTime = endTime[0].split(':');
      endDate.set({ h: endTime[0], m: endTime[1] });
      const currentDate = moment(`${selectedDate.getFullYear()}-${selectedDate.getMonth() + 1}-${selectedDate.getDate()}`, 'YYYY-MM-DD');
      currentDate.set({ h: currentHour.split(':')[0], m: currentHour.split(':')[1] });
      const timeTest = moment(`${currentHour}:00`, 'HH:mm:ss').isBetween(moment(s[1].split('-'), 'HH:mm:ss'), moment(e[1].split('-'), 'HH:mm:ss'));
      if (currentDate.isBetween(startDate, endDate) && timeTest) {
        return true;
      }
    }
    return false;
  }

  /*
  * COMPONENT RENDERING
  */

  renderModals() {
    const {
      bookingModal,
      selectedRoomId,
      selectedRoomName,
      selectedHour,
      selectedRoomCurrentBookings,
      selectedBookingId,
      bookingInfoModal,
      selectedBooking,
      selectedBookingCampons,
    } = this.state;
    const { selectedDate } = this.props;

    return (
      <div className="modals">
        <ReservationDetailsModal
          show={bookingModal}
          selectedRoomId={selectedRoomId}
          selectedRoomName={selectedRoomName}
          selectedHour={selectedHour}
          selectedDate={selectedDate}
          selectedRoomCurrentBookings={selectedRoomCurrentBookings}
          selectedBookingId={selectedBookingId}
          onClose={this.toggleBookingModal}
          onCloseWithReservation={this.toggleBookingModalWithReservation}
        />
        <BookingInfoModal
          show={bookingInfoModal}
          booking={selectedBooking}
          selectedRoomName={selectedRoomName}
          onClose={this.toggleBookingInfoModal}
          onCloseWithAction={this.toggleBookingInfoWithAction}
          campons={selectedBookingCampons}
        />
      </div>
    );
  }

  renderCurrentBookings(bookings) {
    const bookingsDiv = [];

    bookings.forEach((booking) => {
      bookingsDiv.push(
        <Popup
          key={booking.id}
          trigger={
            (
              <div
                className="calendar__booking"
                style={this.setBookingStyle(booking).booking_style}
                role="button"
                tabIndex="0"
                onClick={() => this.handleClickBooking(booking)}
                onKeyDown={() => {}}
              >
                {this.renderBookingText(booking)}
                {/* {campOns.length > 0 ? Cells.renderCampOns(campOns) : ''} */}
              </div>
          )}
          content={Cells.getPopupContent(booking).content}
          flowing
          style={{ padding: '5px' }}
        />,
      );
    });
    return bookingsDiv;
  }

  renderBookingText(booking) {
    const { orientation } = this.props;
    const isRecurring = booking.recurring_booking;
    let usernameDisplay = booking.booker.username;
    if (booking.show_note_on_calendar) {
      usernameDisplay = booking.note;
    } else if (booking.group) {
      usernameDisplay = booking.group.name;
    }

    if (Cells.getBookingDuration(booking) >= 20) {
      return (
        <span>
          {booking.start_time.length > 5
            ? booking.start_time.substring(0, booking.start_time.length - 3) : booking.start_time}
          {' - '}
          {booking.end_time.length > 5
            ? booking.end_time.substring(0, booking.end_time.length - 3) : booking.end_time}
          <br />
          {Cells.getBookingDuration(booking) < 30 && orientation === 1
            ? <span>{usernameDisplay.substring(0, 4)}</span>
            : <span>{usernameDisplay.substring(0, 9)}</span>}
          {booking.note && (booking.display_note || storage.checkAdmin())
            ? Cells.renderNote(booking) : null}

          {booking.confirmed || isRecurring ? (
            <div style={{ marginTop: '5px' }}>
              {isRecurring ? <Icon name="history" flipped="horizontally" /> : null}
              {booking.confirmed ? <Icon name="check circle" /> : null}
            </div>
          ) : null}
        </span>
      );
    }
    return null;
  }

  static renderCampOns(campOns) {
    const text = [
      <span key="-1">
        [CAMPON]
        <br />
      </span>];
    campOns.forEach((campOn) => {
      text.push(
        <span key={campOn.id} className="calendar__cells__cell--campon">
          {campOn.start_time.substring(0, campOn.start_time.length - 3)}
          -
          {campOn.end_time.substring(0, campOn.end_time.length - 3)}
          &nbsp;:&nbsp;
          {campOn.booker.username}
          <br />
        </span>,
      );
    });
    return (
      <span>
        <br />
        {text}
      </span>
    );
  }

  static renderNote(booking) {
    return (
      <Popup
        className="popup--note"
        trigger={(<Icon name="attention" />)}
        content={(
          <Message negative>
            {booking.note}
          </Message>
        )}
      />
    );
  }

  render() {
    const {
      roomsList,
      hoursList,
      bookings,
      unavailabilities,
    } = this.props;
    const cells = [];
    let roomsCells = [];
    let cell = 0;

    for (let i = 0; i < roomsList.length; i += 1) {
      const currentRoom = roomsList[i];
      const roomUnavailability = [];
      unavailabilities.forEach((un) => {
        if (un.room === currentRoom.id) {
          roomUnavailability.push(un);
        }
      });
      for (let j = 0; j < hoursList.length; j += 1) {
        const currentHour = hoursList[j];
        const unavailable = this.checkAvailability(roomUnavailability, currentHour);
        roomsCells.push(
          <div className="calendar__cells__cell" style={this.setCellStyle(j, unavailable).cell_style} role="button" tabIndex="0" key={cell} onClick={() => this.handleClickCell(currentHour, currentRoom)} onKeyDown={() => {}} />,
        );
        cell += 1;
      }

      const bookedCells = [];
      if (bookings) {
        const bookingsList = bookings.filter(booking => booking.room === currentRoom.id);
        if (bookingsList.length > 0) {
          bookedCells.push(this.renderCurrentBookings(bookingsList));
        }
      }

      cells.push(
        <div className="calendar__rooms__cells" key={i} style={this.setStyle().division}>
          {roomsCells}
          {bookedCells}
        </div>,
      );

      roomsCells = [];
    }
    return (
      <div className="calendar__cells__wrapper" style={this.setStyle().wrapper}>
        {cells}
        {this.renderModals()}
      </div>
    );
  }
}

Cells.propTypes = {
  roomsList: PropTypes.instanceOf(Array),
  unavailabilities: PropTypes.instanceOf(Array),
  hoursList: PropTypes.instanceOf(Array),
  hoursSettings: PropTypes.instanceOf(Object),
  bookings: PropTypes.instanceOf(Array),
  selectedDate: PropTypes.instanceOf(Object),
  onCloseModalWithAction: PropTypes.func,
  campOns: PropTypes.instanceOf(Array),
  orientation: PropTypes.number,
  update: PropTypes.func,
};

Cells.defaultProps = {
  roomsList: [],
  unavailabilities: [],
  hoursList: [],
  hoursSettings: {
    start: '08:00',
    end: '23:00',
    increment: 60,
  },
  bookings: [],
  campOns: null,
  selectedDate: new Date(),
  orientation: 0,
  onCloseModalWithAction: () => {},
  update: () => {},
};

export default Cells;
