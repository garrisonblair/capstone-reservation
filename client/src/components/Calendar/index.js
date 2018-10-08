import React, {Component} from 'react';
import settings from '../../config/settings';
import './Calendar.scss';
import ReservationDetailsModal from '../ReservationDetailsModal';


class Calendar extends Component {
  
  state = {
    roomsList: [],
    hoursList: [],
    bookings: [],
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

    /*** Set up rooms list ***/
    let colNumber = 33;
    let rooms = [];
    for (let i = 1; i <= colNumber; i++) {
      rooms.push("H961-" + i);
      this.setState({["H961-" + i]: []});
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

    /*** Set up existing bookings list ***/
    let bookings = [{room: "H961-2", start: "08:10", end: "15:50", booker: 'stud1'},{room: "H961-4", start: "08:00", end: "10:30", booker: 'stud2'}];
    this.setState({bookings: bookings});


    /*** Set up variables in scss ***/
    let gridRowNum = minutesIncrement * hours.length / 10;
    document.documentElement.style.setProperty("--colNum", colNumber);
    document.documentElement.style.setProperty("--rowNum", hours.length);
    document.documentElement.style.setProperty("--cellsDivisionNum", gridRowNum);

  }

  /************ RENDER METHODS *************/

  renderDate() {
    return (
      <div className="calendar__date">
        <span>
          {this.state.selectedDate.toDateString()}
        </span>
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
      let bookings = this.state.bookings.filter(booking => booking.room == currentRoom);
      if (bookings.length > 0) {
        bookedCells.push(this.renderCurrentBookings(bookings))
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
        <div className="calendar__booking" style={this.setBookingStyle(booking).booking_style} key={booking.room + booking.start} onClick={this.handleClickBooking}>
          <div className="calendar__booking__booker"> {booking.booker} </div>
          <div className="calendar__booking__time">
            <div>{booking.start}</div>
            <div>{booking.end}</div>
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
        gridColumn: 1
      }
    }
    return style;
  }

  //Style for .calendar__booking
  setBookingStyle(booking) {
    let bookingStart = this.timeStringToInt(booking.start);
    let bookingEnd = this.timeStringToInt(booking.end);
    let calendarStart = this.timeStringToInt(this.state.hoursSettings.start);

    //Find the rows in the grid the booking corresponds to. Assuming an hour is divided in 6 rows, each representing an increment of 10 minutes.
    let rowStart = ((bookingStart.hour * 60 + bookingStart.minutes) - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;
    let rowEnd = ((bookingEnd.hour * 60 + bookingEnd.minutes) - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;

    let style = {
      booking_style: {
        gridRowStart: rowStart, 
        gridRowEnd: rowEnd,
        gridColumn: 1,
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

  /************ HELPER METHOD *************/

  toggleBookingModal = () => {
    this.setState({isBooking: !this.state.isBooking})
  }

  //Handle time in the string format
  timeStringToInt(time) {
    //Need offset depending if time format is H:MM or HH:MM
    let offset = time.length == 5 ? 1 : 0;

    let timeInt = {
      hour: parseInt(time.substring(0, 1 + offset)),
      minutes: parseInt(time.substring(2 + offset , 4 + offset))
    }
    
    return timeInt;
  }

   /************ COMPONENT RENDERING *************/

  render() {
    return (
      <div className="calendar__container">
        {this.renderDate()}
        <div className="calendar__wrapper">
          {this.renderRooms()}
          {this.renderHours()}
          {this.renderCells()} 
        </div>
        {/* {this.state.isBooking ? <ReservationDetailsModal></ReservationDetailsModal> : null} */}
        <ReservationDetailsModal show={this.state.isBooking} selectedRoom={this.state.selectedRoom} selectedHour={this.state.selectedHour} selectedDate={this.state.selectedDate}></ReservationDetailsModal>
      </div>
    )
  }
}

export default Calendar;
