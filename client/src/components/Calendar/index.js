import React, {Component} from 'react';
import './Calendar.scss';
import ReservationDetailsModal from '../ReservationDetailsModal';
import BookingInfoModal from '../BookingInfoModal';
import api from '../../utils/api';
import {Button, Icon} from 'semantic-ui-react';


class Calendar extends Component {

  state = {
    roomsList: [],
    hoursList: [],
    selectedHour: "",
    selectedRoomName: "",
    selectedRoomId: "",
    selectedRoomCurrentBookings: [],
    selectedDate: new Date(),
    selectedBooking: {},
    bookingModal: false,
    bookingInfoModal: false,
  };

  /************ REQUESTS *************/
  
  //propsTesting* is used for Jest testing 
  getBookings() {
    if(this.props.propsTestingBookings) {
      this.setState({bookings: this.props.propsTestingBookings})
    } else {
      let params = {
        year: this.state.selectedDate.getFullYear(),
        month: this.state.selectedDate.getMonth() + 1,
        day: this.state.selectedDate.getDate()
      }
  
      api.getBookings(params)
      .then((response) => {
        this.setState({bookings: response.data})

      })
      .catch(function (error) {
        console.log(error);
      })
      .then(function () {
      });
    }
    this.getCampOns(params)
  }

  getCampOns(params) {
    if(this.props.propsTestingCampOns) {
      this.setState({campOns: this.props.propsTestingCampOns})
    } else {
      api.getCampOns(params)
      .then((response) => {
        this.setState({campOns: response.data}, () => {
          this.campOnToBooking();
        })
      })
      .catch(function (error) {
        console.log(error);
      })
      .then(function () {
        // always executed
      });
    }
  }

  getRooms() {
    if(this.props.propsTestingRooms) {
      this.setState({roomsList: this.props.propsTestingRooms})
    } else {
      api.getRooms()
      .then((response) => {
        this.setState({roomsList: response.data})
        let colNumber = response.data.length;
        document.documentElement.style.setProperty("--colNum", colNumber);
      })
      .catch(function (error) {
        console.log(error);
      })
      .then(function () {
        // always executed
      });
    } 
  }

  /************ STYLE METHODS*************/

  // Style for .calendar__cells__cell
  setCellStyle(hourRow) {
    const {hoursSettings} = this.state;
    let rowStart = (hourRow * hoursSettings.increment / 10) + 1;
    let rowEnd = rowStart + hoursSettings.increment / 10;

    let style = {
      cell_style: {
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        gridColumn: 1,
        minHeight: '100px',
      }
    }
    return style;
  }

  //Style for .calendar__booking
  setBookingStyle(booking) {
    const {hoursSettings} = this.state;
    let bookingStart = this.timeStringToInt(booking.start_time);
    let bookingEnd = this.timeStringToInt(booking.end_time);
    let calendarStart = this.timeStringToInt(hoursSettings.start);
    let campOn = 1;
    let color = 'yellow'
    if (!!booking.isCampOn) {
      campOn = 100;
      color = 'orange'
    }
    //Find the rows in the grid the booking corresponds to. Assuming an hour is divided in 6 rows, each representing an increment of 10 minutes.
    let rowStart = ((bookingStart.hour * 60 + bookingStart.minutes) - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;
    let rowEnd = ((bookingEnd.hour * 60 + bookingEnd.minutes) - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;

    let style = {
      booking_style: {
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        gridColumn: 1,
        zIndex: campOn,
        backgroundColor: color
      }
    }
    return style;
  }

   /************ CLICK HANDLING METHODS *************/

  handleClickCell = (e) => {
    let selectedRoomId = e.target.getAttribute('data-room-id');
    let selectedRoomName = e.target.getAttribute('data-room-name');
    let selectedHour = e.target.getAttribute('data-hour');
    let selectedRoomCurrentBookings = []
    this.state.bookings.map((booking) => {
      if (booking.room == selectedRoomId) {
        selectedRoomCurrentBookings.push(booking)
      }
    })
    this.setState({
      selectedHour: selectedHour,
      selectedRoomId: selectedRoomId,
      selectedRoomName: selectedRoomName,
      selectedRoomCurrentBookings: selectedRoomCurrentBookings
    });
    this.toggleBookingModal();
  }

  handleClickBooking = (booking) => {
    let roomName = ""
    this.state.roomsList.map((room) => {
      if (room.id == booking.room) {
        roomName = room.room_id
        return
      }
    })
    this.setState({selectedBooking: booking, selectedRoomName: roomName}, () => {
      this.toggleBookingInfoModal();
    })
  }

  handleClickNextDate = (e) => {
    let nextDay = this.state.selectedDate;
    nextDay.setDate(nextDay.getDate() + 1);
    this.setState({selectedDate: nextDay})
    this.getBookings();
  }

  handleClickPreviousDate = (e) => {
    let previousDay = this.state.selectedDate;
    previousDay.setDate(previousDay.getDate() - 1);
    this.setState({selectedDate: previousDay})
    this.getBookings();
  }

  /************ HELPER METHOD *************/
  
  toggleBookingModal = () => {
    this.setState({bookingModal: !this.state.bookingModal})
  }

  toggleBookingInfoModal = () => {
    this.setState({bookingInfoModal: !this.state.bookingInfoModal})
  }

  toggleBookingModalWithReservation = () => {
    //Use reload for now. Might need to change this if we want to view the calendar of the date we made the reservation on.
    //With reload, the view will come back to the current day.
    window.location.reload();
  }

  toggleBookingInfoWithCampOn = () => {
    window.location.reload();
  }

  timeStringToInt(time) {
    let tokens = time.split(':');
    let timeInt = {
      hour: parseInt(tokens[0]),
      minutes: parseInt(tokens[1]),
    }
    return timeInt;
  }

  campOnToBooking = () => {
    const {bookings, campOns} = this.state;
    
      let campOnBookings = []
      if(!!campOns && !!bookings) {
        campOns.map((campOn) => {
          let date = ''
          let room = ''
          if(bookings) {
            for(let i =0; i<bookings.length; i++) {
              if(bookings[i].id == campOn.camped_on_booking) {
                date = bookings[i].date
                room = bookings[i].room
                break
              }
            }
          }
          campOnBookings.push({
            date: date,
            start_time: campOn.start_time,
            end_time: campOn.end_time,
            student: campOn.student,
            room: room,
            id: `camp${campOn.camped_on_booking}`,
            isCampOn: true
          });
        })
        campOnBookings.map((campOnBooking) => {
          bookings.push(campOnBooking)
        })
        this.setState({bookings: bookings})
      }
  }

  /************* COMPONENT LIFE CYCLE *************/

  componentDidMount() {
    // console.log(settings)
  }

  componentWillMount() {
    /*** Get bookings ***/
    this.getBookings();

    /*** Get rooms ***/
    this.getRooms();

    /*** Set up hours ***/
    let hoursSettings = {
      start: "08:00",
      end: "23:00",
      increment: 60
    }
    let hourStart =  this.timeStringToInt(hoursSettings.start);
    let hourEnd =  this.timeStringToInt(hoursSettings.end);

    let minutesIncrement = hoursSettings.increment;
    let hours = []
    let time = new Date();
    time.setHours(hourStart.hour, hourStart.minutes, 0);

    //Format time for display in table
    let currentTime = hourStart.hour * 60 + hourStart.minutes;
    let endTime = hourEnd.hour * 60 + hourEnd.minutes;

    while (currentTime <= endTime) {
      hours.push(time.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}));
      time.setMinutes(time.getMinutes() + minutesIncrement);
      currentTime += minutesIncrement;
    }
    this.setState({hoursSettings: hoursSettings, hoursList: hours});

    /*** Set up variables in scss ***/
    let gridRowNum = minutesIncrement * hours.length / 10;

    document.documentElement.style.setProperty("--rowNum", hours.length);
    document.documentElement.style.setProperty("--cellsDivisionNum", gridRowNum);
  }

  /************ COMPONENT RENDERING *************/

  renderDate() {
    return (
      <div className="calendar__date">
        <Button
          basic
          circular
          icon="chevron left"
          size="large"
          onClick={this.handleClickPreviousDate}
        />
        <h1 className="calendar__date__header">
          <Icon name="calendar alternate outline" />
          {this.state.selectedDate.toDateString()}
        </h1>
        <Button
          basic
          circular
          icon="chevron right"
          size="large"
          onClick={this.handleClickNextDate}
        />
      </div>
    );
  }

  renderRooms() {
    const {roomsList} = this.state;
    const rooms = roomsList.map((room) =>
      <div className="calendar__rooms__room" key={room.room_id}>
        {room.room_id}
      </div>
    );

    return <div className="calendar__rooms__wrapper">{rooms}</div>
  }

  renderHours() {
    const {hoursList} = this.state;
    const hours = hoursList.map((hour) =>
      <div className="calendar__hours__hour" key={hour}>
        {hour}
      </div>
    );

    return <div className="calendar__hours__wrapper">{hours}</div>
  }

  renderCells() {
    const {roomsList, hoursList} = this.state;

    let cells = [];
    let roomsCells = [];
    let cell = 0;

    for (let i = 0; i < roomsList.length; i++) {
      let currentRoom = roomsList[i];
      for (let j = 0; j < hoursList.length; j++) {
        let currentHour = hoursList[j];
        roomsCells.push(
          <div className="calendar__cells__cell" style={this.setCellStyle(j).cell_style} key={cell} data-hour={currentHour} data-room-id={currentRoom.id} data-room-name={currentRoom.room_id} onClick={this.handleClickCell}></div>
        );
        cell++;
      }

      let bookedCells = [];
      if (this.state.bookings) {
        let bookings = this.state.bookings.filter(booking => booking.room == currentRoom.id);
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
      bookingsDiv.push(
        <div className="calendar__booking" style={this.setBookingStyle(booking).booking_style} key={booking.id} data-id={booking.id} data-start-time= {booking.start_time} data-end-time={booking.end_time} onClick={() => this.handleClickBooking(booking)}>
          {/* { !!booking.isCampOn ? <span>[CAMP ON]</span> : null }
          <div className="calendar__booking__booker">{booking.student} </div>
          <div className="calendar__booking__time">
            <div>{booking.start_time.length > 5 ? booking.start_time.substring(0, booking.start_time.length-3): booking.start_time}</div>
            <div>{booking.end_time.length > 5 ? booking.end_time.substring(0, booking.end_time.length-3): booking.end_time}</div>
          </div> */}

          {booking.start_time.length > 5 ? booking.start_time.substring(0, booking.start_time.length-3): booking.start_time} - {booking.end_time.length > 5 ? booking.end_time.substring(0, booking.end_time.length-3): booking.end_time}
          <br/>
          { !!booking.isCampOn ? <span>[CAMP ON]<br/></span> : null }
          <span>{booking.student}</span>
        </div>
      )
    });
    return bookingsDiv;
  }

  render() {
    return (
      <div className="calendar__container">
        {this.renderDate()}
        <div className="calendar__wrapper">
          {this.renderRooms()}
          {this.renderHours()}
          {this.renderCells()}
        </div>
        <ReservationDetailsModal
          show={this.state.bookingModal}
          selectedRoomId={this.state.selectedRoomId}
          selectedRoomName={this.state.selectedRoomName}
          selectedHour={this.state.selectedHour}
          selectedDate={this.state.selectedDate}
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
          onCloseWithCampOn={this.toggleBookingInfoWithCampOn}
        />
      </div>
    )
  }
}

export default Calendar;
