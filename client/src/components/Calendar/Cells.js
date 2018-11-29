import PropTypes from 'prop-types';
import React, { Component } from 'react';
import './Calendar.scss';
import ReservationDetailsModal from '../ReservationDetailsModal';
import BookingInfoModal from '../BookingInfoModal';


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
    bookingModal: false,
    bookingInfoModal: false,
  };

  /*
   *COMPONENT LIFE CYCLE
   */

  static getDerivedStateFromProps(props, state) {
    if (props.bookings === state.bookings) {
      return null;
    }
    return {
      bookings: props.bookings,
    };
  }

  /*
   * STYLE METHODS
   */

  // Style for .calendar__cells__cell
  setCellStyle(hourRow) {
    const { hoursSettings } = this.props;
    const rowStart = (hourRow * hoursSettings.increment / 10) + 1;
    const rowEnd = rowStart + hoursSettings.increment / 10;
    const height = '75px';

    const style = {
      cell_style: {
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        height,
      },
    };
    return style;
  }

  // Style for .calendar__booking
  setBookingStyle(booking, campOnsNumber) {
    const {hoursSettings} = this.props;
    let bookingStart = this.timeStringToInt(booking.start_time);
    let bookingEnd = this.timeStringToInt(booking.end_time);
    let calendarStart = this.timeStringToInt(hoursSettings.start);
    let color = '#5a9ab2';
    let currentDate = (new Date());
    let currentMinute = currentDate.getMinutes() < 10 ? `0${currentDate.getMinutes()}` : `${currentDate.getMinutes()}`;

    //Change booking color if it's passed
    let bookingDate = booking.date.split("-");
    let datePassed = false;
    let sameDate = false
    if (parseInt(bookingDate[0]) < currentDate.getFullYear()) {
      datePassed = true;
    } else {
      if (parseInt(bookingDate[0]) == currentDate.getFullYear()) {
        if (parseInt(bookingDate[1]) < currentDate.getMonth() + 1) {
          datePassed = true;
        } else {
          if (parseInt(bookingDate[1]) == currentDate.getMonth() + 1) {
            if (parseInt(bookingDate[2]) < currentDate.getDate()) {
              datePassed = true;
            } else {
              if (parseInt(bookingDate[2]) == currentDate.getDate()) {
                sameDate = true
              }
            }
          }
        }
      }
    }
    if (datePassed || (sameDate && parseInt(booking.end_time.replace(/:/g, '')) <= parseInt(`${currentDate.getHours()}${currentMinute}00`))) {
      color = 'rgb(114, 120, 126)'
    } else {
      if (campOnsNumber > 0) {
        color = '#77993b'
      }
    }

    // Find the rows in the grid the booking corresponds to.
    // Assuming an hour is divided in 6 rows, each representing an increment of 10 minutes.
    const rowStart = ((bookingStart.hour * 60 + bookingStart.minutes)
                      - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;
    const rowEnd = ((bookingEnd.hour * 60 + bookingEnd.minutes)
                    - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;

    const style = {
      booking_style: {
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        gridColumn: 1,
        backgroundColor: color,
      },
    };
    return style;
  }

  /*
  * HELPER METHOD
  */

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

  toggleBookingModal = () => {
    const { bookingModal } = this.state;
    this.setState({ bookingModal: !bookingModal });
  }

  toggleBookingInfoModal = () => {
    const { bookingInfoModal } = this.state;
    this.setState({ bookingInfoModal: !bookingInfoModal });
  }

  toggleBookingModalWithReservation = () => {
    const { onCloseModalWithAction } = this.props;
    this.setState({ bookingModal: false, bookingInfoModal: false });
    onCloseModalWithAction();
  }

  toggleBookingInfoWithAction = () => {
    const { onCloseModalWithAction } = this.props;
    this.setState({ bookingModal: false, bookingInfoModal: false });
    onCloseModalWithAction();
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
    const { roomsList } = this.props;
    let roomName = '';
    roomsList.forEach((room) => {
      if (room.id === booking.room) {
        roomName = room.name;
        // return;
      }
    });
    this.setState({ selectedBooking: booking, selectedRoomName: roomName }, () => {
      this.toggleBookingInfoModal();
    });
  }

  /*
  * COMPONENT RENDERING
  */

  renderCells() {
    const { roomsList, hoursList, bookings } = this.props;

    const cells = [];
    let roomsCells = [];
    let cell = 0;

    for (let i = 0; i < roomsList.length; i += 1) {
      const currentRoom = roomsList[i];
      for (let j = 0; j < hoursList.length; j += 1) {
        const currentHour = hoursList[j];
        roomsCells.push(
          <div className="calendar__cells__cell" style={this.setCellStyle(j).cell_style} role="button" tabIndex="0" key={cell} onClick={() => this.handleClickCell(currentHour, currentRoom)} onKeyDown={() => {}} />,
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
        <div className="calendar__rooms__cells" key={i}>
          {roomsCells}
          {bookedCells}
        </div>,
      );

      roomsCells = [];
    }
    return <div className="calendar__cells__wrapper">{cells}</div>;
  }

  renderCurrentBookings(bookings) {
    const bookingsDiv = [];

    bookings.forEach((booking) => {
      const campOns = this.getCamponsForBooking(booking);
      bookingsDiv.push(
        <div className="calendar__booking" style={this.setBookingStyle(booking, campOns.length).booking_style} role="button" tabIndex="0" key={booking.id} onClick={() => this.handleClickBooking(booking)} onKeyDown={() => {}}>
          {booking.start_time.length > 5
            ? booking.start_time.substring(0, booking.start_time.length - 3) : booking.start_time}
          {' - '}
          {booking.end_time.length > 5
            ? booking.end_time.substring(0, booking.end_time.length - 3) : booking.end_time}
          <br />
          {(booking.end_time.replace(/:/g, '') - booking.start_time.replace(/:/g, '')) < 4000 ? null : <span>{booking.booker.user.username}</span>}
          {campOns.length > 0 ? Cells.renderCampOns(campOns) : ''}
        </div>,
      );
    });
    return bookingsDiv;
  }

  static renderCampOns(campOns) {
    const text = [
      <span key="-1">
        [CAMP]
        <br />
      </span>];
    campOns.forEach((campOn) => {
      text.push(
        <span key={campOn.id}>
          {campOn.start_time.substring(0, campOn.start_time.length - 3)}
          -
          {campOn.end_time.substring(0, campOn.end_time.length - 3)}
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

  render() {
    const {
      bookingModal,
      selectedRoomId,
      selectedRoomName,
      selectedHour,
      selectedRoomCurrentBookings,
      selectedBookingId,
      bookingInfoModal,
      selectedBooking,
    } = this.state;
    const { selectedDate } = this.props;
    return (
      <div>
        {this.renderCells()}

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
        />
      </div>
    );
  }
}

Cells.propTypes = {
  roomsList: PropTypes.instanceOf(Array),
  hoursList: PropTypes.instanceOf(Array),
  hoursSettings: PropTypes.instanceOf(Object),
  bookings: PropTypes.instanceOf(Array),
  selectedDate: PropTypes.instanceOf(Object),
  onCloseModalWithAction: PropTypes.func,
  campOns: PropTypes.instanceOf(Array),
};

Cells.defaultProps = {
  roomsList: [],
  hoursList: [],
  hoursSettings: {
    start: '08:00',
    end: '23:00',
    increment: 60,
  },
  bookings: [],
  campOns: null,
  selectedDate: new Date(),
  onCloseModalWithAction: () => {},
};

export default Cells;
