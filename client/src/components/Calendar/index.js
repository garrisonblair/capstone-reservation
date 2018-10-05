import React, {Component} from 'react';
import settings from '../../config/settings';
import './Calendar.scss';


class Calendar extends Component {
  
  state = {
    roomsList: [],
    hoursList: [],
    dateSelected: new Date(),
    bookings: [{room: "H961-2", start: 8, end: 15, booker: 'stud1'},{room: "H961-4", start: 10, end: 20, booker: 'stud2'}]
  };

  componentDidMount() {
    console.log(settings)
  }

  componentWillMount() {
    // Set up rooms list
    let colNumber = 33;
    let rooms = [];
    for (let i = 1; i <= colNumber; i++) {
      rooms.push("H961-" + i);
      this.setState({["H961-" + i]: []});
    }
    this.setState({roomsList: rooms});

    // Set up hours
    let hourStart =  8;
    let hourEnd =  24;
    let minutesIncrement = 60;
    let hours = []
    let time = new Date();
    time.setHours(hourStart,0,0);

    while (time.getDay() == this.state.dateSelected.getDay()) {
      hours.push(time.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}));
      time.setMinutes(time.getMinutes() + minutesIncrement);
    }
  
    this.setState({hoursList: hours, minutesIncrement: minutesIncrement});

    //Set variables in scss
    
    document.documentElement.style.setProperty("--colNum", colNumber);
    document.documentElement.style.setProperty("--rowNum", hours.length);
    document.documentElement.style.setProperty("--cellsDivisionNum", minutesIncrement * (hourEnd - hourStart) / 10);

  }

  renderDate() {
    return (
      <div className="calendar__date">
        <span>
          {this.state.dateSelected.toDateString()}
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
          <div className="calendar__cells__cell" style={this.setCellStyle(j).cell_style} key={cell} data-hour={currentHour} data-room={currentRoom} onClick={this.handleClickCell}>{this.cellText(currentRoom, currentHour)}</div>
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
    let date = new Date();
    let bookingStart, bookingEnd;
    console.log(date)
    date.setH
    console.log(bookings[0].start - bookings[0].end)


    bookings.forEach(booking => {
      
      let style = {
        //Assuming each hour div is divided in 6 rows for an increment of 10 minutes
        cell_style: {
          gridRowStart: booking.start, 
          gridRowEnd: booking.end,
          gridColumn: 1,
        }
      }

      bookingsDiv.push(
        <div className="calendar__cells__event" style={style.cell_style} key={booking.room + booking.start}>
          <div className="calendar__cells__event__booker"> {booking.booker} </div>
          <div className="calendar__cells__event__time">
            <div>{`HH:MM XM`}</div>
            <div>{`HH:MM XM`}</div>
          </div>

        </div>
        )
    });

    return bookingsDiv;
  }

  setCellStyle(x) {
    // Style for .calendar__cells_cell
    let style = {
      //Assuming each hour div is divided in 6 rows for an increment of 10 minutes
      cell_style: {
        gridRowStart: x * 6 + 1,
        gridRowEnd: (x + 1) * 6 + 1,
        gridColumn: 1
      }
    }
    return style;
  }

  cellText = (room, hour) => {
    let roomHours = this.state[room];

    for (let i = 0 ;i < roomHours.length; i++) {
      if (roomHours[i] == hour) {
        return "Booked by Student 1 from 10:50 to 11:50";
      }
    }

    return "";
  }

  handleClickCell = (e) => {
    let selectedRoom = e.target.getAttribute('data-room');
    let selectedHour = e.target.getAttribute('data-hour');
    
    alert("open modal for room " + selectedRoom + ", starting at " + selectedHour)
    // let roomHours = this.state[selectedRoom];

    // if (!roomHours.includes(selectedHour)) {
    //   roomHours.push(selectedHour);
    //   this.setState({[selectedRoom]:  roomHours});
    // } else {
    //   // This is for delete or CAMPON maybe
    //   let filteredHours = roomHours.filter(hour => hour !== selectedHour)
    //   this.setState({[selectedRoom]: filteredHours});
    // }
    
    
  }

  handleClickBooking(e) {
    console.log(e)
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
      </div>
    )
  }
}

export default Calendar;
