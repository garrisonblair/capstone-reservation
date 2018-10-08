import React, {Component} from 'react';
import settings from '../../config/settings';
import './Calendar.scss';
import ReservationDetailsModal from '../ReservationDetailsModal';
import axios from 'axios';
import { Button, Item } from 'semantic-ui-react';


class Calendar extends Component {

  state = {
    roomsList: [],
    hoursList: [],
    isBooking: false,
    selectedHour: "",
    selectedRoom: "",
    selectedDate: new Date()
  };

   /************ SETUP *************/

  componentDidMount() {
    console.log(settings)
  }

  //TODO: Get settings from props or from requests.
  componentWillMount() {
    /*** Get bookings ***/
    this.getBookings();

    /*** Set up rooms list ***/
    let colNumber = 10;
    let rooms = [];
    for (let i = 1; i <= colNumber; i++) {
      rooms.push(i);
      // this.setState({["H961-" + i]: []});
    }
    this.setState({roomsList: rooms});
    /*** Set up hours ***/
    let hoursSettings = {
      start: "08:00",
      end: "23:00",
      increment: 30
    }
    let hourStart =  this.timeStringToInt(hoursSettings.start);
    let hourEnd =  this.timeStringToInt(hoursSettings.end);

    let minutesIncrement = hoursSettings.increment;
    let hours = []
    let time = new Date();
    time.setHours(hourStart.hour,hourStart.minutes,0);

    //Format time for display in table
    let currentTime = hourStart.hour * 60 + hourStart.minutes;
    let endTime = hourEnd.hour * 60 + hourEnd.minutes;

    //TODO: Remove loop variable. Using this var only to avoid infinite loop during development.
    let loop = 0;
    while (currentTime <= endTime && loop < 1000) {
      hours.push(time.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}));
      time.setMinutes(time.getMinutes() + minutesIncrement);
      currentTime += minutesIncrement;
      loop ++;
      if (loop > 999) {
        alert("Infinite loop")
      }
    }
    this.setState({hoursSettings: hoursSettings, hoursList: hours});

    /*** Set up variables in scss ***/
    let gridRowNum = minutesIncrement * hours.length / 10;
    document.documentElement.style.setProperty("--colNum", colNumber);
    document.documentElement.style.setProperty("--rowNum", hours.length);
    document.documentElement.style.setProperty("--cellsDivisionNum", gridRowNum);

  }

  /************ REQUESTS *************/
  getBookings(){
    let params = {
      year: this.state.selectedDate.getFullYear(),
      month: this.state.selectedDate.getMonth() + 1,
      day: this.state.selectedDate.getDate()
    }

    axios({
      method: 'GET',
      url: `${settings.API_ROOT}/booking`,
      params: params
    })
    .then((response) => {
      let bookings = [];
      response.data.map(booking => {
        bookings.push(booking);
      })

      this.setState({bookings: response.data})

      // this.setState({bookings: response})
    })
    .catch(function (error) {
      console.log(error);
    })
    .then(function () {
      // always executed
    });  
  }

  /************ RENDER METHODS *************/

  // TODO: Styling the buttons
  renderDate() {
    return (
      <div className="calendar__date">
        <Button onClick={this.handleClickPreviousDate}>Previous</Button>
        <span>
          {this.state.selectedDate.toDateString()}
        </span>
        <Button onClick={this.handleClickNextDate}>Next</Button>
      </div>
    );
  }

  renderRooms() {
    const { roomsList } = this.state;

    const rooms = roomsList.map((room) =>
      <div className="calendar__rooms__room" key={room}>
        {room}
      </div>
    );

    return  <div className="calendar__rooms__wrapper">{rooms}</div>

  }

  renderHours() {
    const { hoursList } = this.state;
    const hours = hoursList.map((hour) =>
      <div className="calendar__hours__hour" key={hour}>
        {hour}
      </div>
    );

    return <div className="calendar__hours__wrapper">{hours}</div>
  }

  renderCells() {
    const { roomsList, hoursList } = this.state;

    let cells = [];
    let roomsCells = [];
    let cell = 0;

    for (let i = 0; i < roomsList.length; i++) {
      let currentRoom = roomsList[i];
      for (let j = 0; j < hoursList.length; j++) {
        let currentHour = hoursList[j];
        roomsCells.push(
          <div className="calendar__cells__cell" style={this.setCellStyle(j).cell_style} key={cell} data-hour={currentHour} data-room={currentRoom} onClick={this.handleClickCell}></div>
        );
        cell++;
      }

      let bookedCells = [];
      if (this.state.bookings) {     
        let bookings = this.state.bookings.filter(booking => booking.room == currentRoom);
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
        <div className="calendar__booking" style={this.setBookingStyle(booking).booking_style} key={booking.id} onClick={this.handleClickBooking}>
          <div className="calendar__booking__booker">{booking.student} </div>
          <div className="calendar__booking__time">
            <div>{booking.start_time.length > 5 ? booking.start_time.substring(0, booking.start_time.length-3): booking.start_time}</div>
            <div>{booking.end_time.length > 5 ? booking.end_time.substring(0, booking.end_time.length-3): booking.end_time}</div>
          </div>

        </div>
        )
    });

    return bookingsDiv;
  }


  /************ STYLE METHODS*************/


  // Style for .calendar__cells__cell
  setCellStyle(hourRow) {

    let rowStart = (hourRow * this.state.hoursSettings.increment / 10) + 1;
    let rowEnd = rowStart + this.state.hoursSettings.increment / 10;

    let style = {
      cell_style: {
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        gridColumn: 1,
        minHeight: '50px'
      }
    }
    return style;
  }

  //Style for .calendar__booking
  setBookingStyle(booking) {
    let bookingStart = this.timeStringToInt(booking.start_time);
    let bookingEnd = this.timeStringToInt(booking.end_time);
    let calendarStart = this.timeStringToInt(this.state.hoursSettings.start);

    //Find the rows in the grid the booking corresponds to. Assuming an hour is divided in 6 rows, each representing an increment of 10 minutes.
    let rowStart = ((bookingStart.hour * 60 + bookingStart.minutes) - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;
    let rowEnd = ((bookingEnd.hour * 60 + bookingEnd.minutes) - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;

    let style = {
      booking_style: {
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        gridColumn: 1
      }
    }
    return style;
  }

   /************ CLICK HANDLING METHODS *************/

  //TODO: Add modal opening when clicking on empty time slot
  handleClickCell = (e) => {
    let selectedRoom = e.target.getAttribute('data-room');
    let selectedHour = e.target.getAttribute('data-hour');

    this.toggleBookingModal();
    this.setState({selectedHour: selectedHour, selectedRoom: selectedRoom});
  }

  // TODO: Handle click on an existing booking
  handleClickBooking = (e) => {
    console.log(e)
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
    this.setState({isBooking: !this.state.isBooking})
  }

  //Handle time in the string format
  timeStringToInt(time) {
    //Need offset depending if time format is H:MM or HH:MM
    let offset = time.charAt(2) == ':' ? 0 : 1;

    let timeInt = {
      hour: parseInt(time.substring(0, 2 - offset)),
      minutes: parseInt(time.substring(3 - offset , 5 - offset))
    }

    return timeInt;
  }

   /************ COMPONENT RENDERING *************/


  render() {
    return this.state.bookings ? (
      <div className="calendar__container">
        {this.renderDate()}
        <div className="calendar__wrapper">
          {this.renderRooms()}
          {this.renderHours()}
          {this.renderCells()}
        </div>
        {/* {this.state.isBooking ? <ReservationDetailsModal></ReservationDetailsModal> : null} */}
        <ReservationDetailsModal
          show={this.state.isBooking}
          selectedRoom={this.state.selectedRoom}
          selectedHour={this.state.selectedHour}
          selectedDate={this.state.selectedDate}
          onClose={this.toggleBookingModal}
        />
      </div>
    ) : (
      <span>Fetching bookings</span>
    )
  }
}

export default Calendar;
