import React, {Component} from 'react';
import './Calendar.scss';
import SelectedDate from './SelectedDate';
import Rooms from './Rooms';
import Hours from './Hours';
import Cells from './Cells';
import api from '../../utils/api';


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
    if(!!this.props.propsTestingBookings) {
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

  /************ HELPER METHOD *************/

  changeDate = (date) => {
    this.setState({selectedDate: date}, () => {
      this.getBookings();
    });
  }
  
  onCloseModalWithAction = () => {
    this.getBookings();
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

  /************* COMPONENT LIFE CYCLE *************/
  componentWillUnmount() {
    document.body.style.backgroundColor = "white";
  }

  componentDidMount() {
    document.body.style.backgroundColor = "#3d3d3e";

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

  render() {
    return (
      <div className="calendar__container">
        <SelectedDate changeDate={this.changeDate} />
        <div className="calendar__wrapper">
          <Rooms roomsList={this.state.roomsList} />
          <Hours hoursList={this.state.hoursList} />
          <Cells 
            hoursSettings={this.state.hoursSettings}
            bookings={this.state.bookings}
            roomsList={this.state.roomsList}
            hoursList={this.state.hoursList}
            campOns={this.state.campOns}
            selectedDate={this.state.selectedDate}
            onCloseModalWithAction={this.onCloseModalWithAction}
          />
        </div>
      </div>
    )
  }
}

export default Calendar;
