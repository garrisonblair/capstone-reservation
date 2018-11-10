import React, {Component} from 'react';
import './Calendar.scss';
import ReservationDetailsModal from '../ReservationDetailsModal';
import BookingInfoModal from '../BookingInfoModal';
import Rooms from './Rooms';
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
        this.getCampOns(params)
      })
      .catch(function (error) {
        console.log(error);
      })
      .then(function () {
      });
    }
  }

  getCampOns(params) {
    if(this.props.propsTestingCampOns) {
      this.setState({campOns: this.props.propsTestingCampOns})
    } else {
      api.getCampOns(params)
      .then((response) => {
        this.setState({campOns: response.data}, () => {
          // this.campOnToBooking();
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
      }
    }
    return style;
  }

  //Style for .calendar__booking
  setBookingStyle(booking, campOnsNumber) {
    const {hoursSettings} = this.state;
    let bookingStart = this.timeStringToInt(booking.start_time);
    let bookingEnd = this.timeStringToInt(booking.end_time);
    let calendarStart = this.timeStringToInt(hoursSettings.start);
    let color = '#5a9ab2'
    if (campOnsNumber > 0) {
      color = '#77993b'
    }
    //Find the rows in the grid the booking corresponds to. Assuming an hour is divided in 6 rows, each representing an increment of 10 minutes.
    let rowStart = ((bookingStart.hour * 60 + bookingStart.minutes) - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;
    let rowEnd = ((bookingEnd.hour * 60 + bookingEnd.minutes) - (calendarStart.hour * 60 + calendarStart.minutes)) / 10 + 1;

    let style = {
      booking_style: {
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        gridColumn: 1,
        backgroundColor: color
      }
    }
    return style;
  }

   /************ CLICK HANDLING METHODS *************/

  handleClickCell = (currentHour, currentRoom) => {
    let selectedRoomId = `${currentRoom.id}`;
    let selectedRoomName = currentRoom.room_id;
    let selectedHour = currentHour;
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
    this.getBookings();
    this.setState({bookingModal: false, bookingInfoModal: false})
  }

  toggleBookingInfoWithAction = () => {
    this.getBookings();
    this.setState({bookingModal: false, bookingInfoModal: false})
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
            booker: campOn.booker,
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

  getCamponsForBooking(booking) {
    let campOns = []
    if(!!this.state.campOns) {
      this.state.campOns.map((campOn) => {
        if(campOn.camped_on_booking == booking.id) {
          campOns.push(campOn)
        }
      })
    }
    return campOns
  }

  /************* COMPONENT LIFE CYCLE *************/

  componentDidMount() {
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
          color="olive"
          icon="chevron left"
          size="tiny"
          onClick={this.handleClickPreviousDate}
        />
        <h3 className="calendar__date__header">
          <Icon name="calendar alternate outline" />
          {this.state.selectedDate.toDateString()}
        </h3>
        <Button
          basic
          circular
          color="olive"
          icon="chevron right"
          size="tiny"
          onClick={this.handleClickNextDate}
        />
      </div>
    );
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
          <div className="calendar__cells__cell" style={this.setCellStyle(j).cell_style} key={cell} onClick={() => this.handleClickCell(currentHour, currentRoom)}></div>
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
      let campOns = this.getCamponsForBooking(booking);
      bookingsDiv.push(
        <div className="calendar__booking" style={this.setBookingStyle(booking, campOns.length).booking_style} key={booking.id} onClick={() => this.handleClickBooking(booking)}>
          {booking.start_time.length > 5 ? booking.start_time.substring(0, booking.start_time.length-3): booking.start_time} - {booking.end_time.length > 5 ? booking.end_time.substring(0, booking.end_time.length-3): booking.end_time}
          <br/>        
          <span>{booking.booker.user.username}</span>
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
      <div className="calendar__container">
        {this.renderDate()}
        <div className="calendar__wrapper">
          <Rooms roomsList={this.state.roomsList} />
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
          onCloseWithAction={this.toggleBookingInfoWithAction}
        />
      </div>
    )
  }
}

export default Calendar;
