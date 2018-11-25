import PropTypes from 'prop-types';
import React, { Component } from 'react';
import './Calendar.scss';
import ReservationDetailsModal from '../ReservationDetailsModal';
import BookingInfoModal from '../BookingInfoModal';


class Cells extends Component {
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
    const { hoursSettings } = this.props;
    const bookingStart = this.timeStringToInt(booking.start_time);
    const bookingEnd = this.timeStringToInt(booking.end_time);
    const calendarStart = this.timeStringToInt(hoursSettings.start);
    let color = '#5a9ab2';
    const currentDate = (new Date());
    const currentMinute = currentDate.getMinutes() < 10 ? `0${currentDate.getMinutes()}` : `${currentDate.getMinutes()}`;
    if (campOnsNumber > 0) {
      color = '#77993b';
    }
    if (booking.date.substring(8, 10) !== (new Date()).getDate() || parseInt(booking.end_time.replace(/:/g, ''), 10) <= parseInt(`${currentDate.getHours()}${currentMinute}00`, 10)) {
      color = 'rgb(114, 120, 126)';
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
  * HELPER METHOD
  */

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

  timeStringToInt(time) {
    let tokens = time.split(':');
    let timeInt = {
      hour: parseInt(tokens[0]),
      minutes: parseInt(tokens[1]),
    }
    return timeInt;
  }


  getCamponsForBooking(booking) {
    let campOns = []
    if(!!this.props.campOns) {
      this.props.campOns.map((campOn) => {
        if(campOn.camped_on_booking == booking.id) {
          campOns.push(campOn)
        }
      })
    }
    return campOns
  }

  /************* COMPONENT LIFE CYCLE *************/

  static getDerivedStateFromProps(props, state) {
    if(props.bookings === state.bookings) {
      return null;
    }
    return {
      bookings: props.bookings,
    };
  }

  /************ COMPONENT RENDERING *************/

  renderCells() {
    const {roomsList, hoursList} = this.props;

    let cells = [];
    let roomsCells = [];
    let cell = 0;

    for (let i = 0; i < roomsList.length; i++) {
      let currentRoom = roomsList[i];
      for (let j = 0; j < hoursList.length; j++) {
        let currentHour = hoursList[j];
        roomsCells.push(
          <div className="calendar__cells__cell" style={this.setCellStyle(j).cell_style} key={cell} onClick={() => this.handleClickCell(currentHour, currentRoom)}></div>
        );
        cell++;
      }

      let bookedCells = [];
      if (this.props.bookings) {
        let bookings = this.props.bookings.filter(booking => booking.room == currentRoom.id);
        if (bookings.length > 0) {
        bookedCells.push(this.renderCurrentBookings(bookings))
        }
      }

      cells.push(
        <div className="calendar__rooms__cells" key={i}>{roomsCells}{bookedCells}</div>
      );

      roomsCells = [];
    }
    return <div className="calendar__cells__wrapper">{cells}</div>;
  }

  renderCurrentBookings(bookings) {
    let bookingsDiv = [];

    bookings.forEach(booking => {
      let campOns = this.getCamponsForBooking(booking);
      bookingsDiv.push(
        <div className="calendar__booking" style={this.setBookingStyle(booking, campOns.length).booking_style} key={booking.id} onClick={() => this.handleClickBooking(booking)}>
          {booking.start_time.length > 5 ? booking.start_time.substring(0, booking.start_time.length-3): booking.start_time} - {booking.end_time.length > 5 ? booking.end_time.substring(0, booking.end_time.length-3): booking.end_time}
          <br/>
          {(booking.end_time.replace(/:/g, '') - booking.start_time.replace(/:/g, '')) < 4000 ? null : <span>{booking.booker.user.username}</span>}
          {campOns.length > 0 ? this.renderCampOns(campOns) : ''}
        </div>
      )
    });
    return bookingsDiv;
  }

  renderCampOns(campOns) {
    let text = [<span key='-1'>[CAMP]<br/></span>]
    campOns.forEach(campOn => {
      text.push(
        <span key={campOn.id}>{campOn.start_time.substring(0, campOn.start_time.length-3)} - {campOn.end_time.substring(0, campOn.end_time.length-3)}<br/></span>
      )
    })
    return <span><br/>{text}</span>
  }

  render() {
    return (
      <div>
        {this.renderCells()}

        <ReservationDetailsModal
          show={this.state.bookingModal}
          selectedRoomId={this.state.selectedRoomId}
          selectedRoomName={this.state.selectedRoomName}
          selectedHour={this.state.selectedHour}
          selectedDate={this.props.selectedDate}
          selectedRoomCurrentBookings={this.state.selectedRoomCurrentBookings}
          selectedBookingId={this.state.selectedBookingId}
          onClose={this.toggleBookingModal}
          onCloseWithReservation={this.toggleBookingModalWithReservation}
        />

        <BookingInfoModal
          show={this.state.bookingInfoModal}
          booking={this.state.selectedBooking}
          selectedRoomName={this.state.selectedRoomName}
          onClose={this.toggleBookingInfoModal}
          onCloseWithAction={this.toggleBookingInfoWithAction}
        />
      </div>
    )
  }
}

Cells.propTypes = {
  roomsList: PropTypes.array,
  hoursList: PropTypes.array,
  hoursSettings: PropTypes.object,
  bookings: PropTypes.array,
  campOns: PropTypes.array,
  selectedDate: PropTypes.object,
  onCloseModalWithAction: PropTypes.func,
}

Cells.defaultProps = {
  roomsList: [],
  hoursList: [],
  hoursSettings: {
                    start: "08:00",
                    end: "23:00",
                    increment: 60
                  },
  bookings: [],
  campOns: [],
  selectedDate: new Date(),
}

export default Cells;
