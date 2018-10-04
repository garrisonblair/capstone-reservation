import React, {Component} from 'react';
import settings from '../../config/settings';
import './Calendar.scss';


class Calendar extends Component {
  
  state = {
    roomsList: [],
    hoursList: [],
    dateSelected: new Date(),
    status: 0
  };

  componentDidMount() {
    console.log(settings)
  }

  componentWillMount() {
    // Set up rooms list
    let colNumber = 10;
    let rooms = [];
    for (let i = 1; i <= colNumber; i++) {
      rooms.push("H961-" + i);
      this.setState({["H961-" + i]: []});
    }
    this.setState({roomsList: rooms});
    document.documentElement.style.setProperty("--colNum", colNumber);

    // Set up hours
    let hourStart =  8;
    let hourEnd =  14;
    let hourIncrement = 1;
    let hours = []

    for (let hour = hourStart; hour <= hourEnd; hour += hourIncrement) {
      hours.push(hour);  
    }
    this.setState({hoursList: hours});
    document.documentElement.style.setProperty("--rowNum", hours.length);

  }

  renderHeader() {
    return (
      <div className="date__header">
        <span>
          {this.state.dateSelected.toDateString()}
        </span>
      </div>
    );
  }

  renderRooms() {
    const { roomsList } = this.state;
    console.log(roomsList)

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
      for (let j = 0; j < hoursList.length; j++) {
        roomsCells.push(
          <div className={`calendar__cells__cell-${j} ${
            this.isBooked(roomsList[i], hoursList[j])
              ? "booked"
              : ""
          }`} style={this.setCellStyle(j).cell_style} key={cell} data-hour={hoursList[j]} data-room={roomsList[i]} onClick={this.handleClickCell}>{this.cellText(roomsList[i], hoursList[j])}</div>
        );
        cell++;
      }
      
      cells.push(
        <div className="calendar__rooms__cells" key={i}>{roomsCells}</div>
      );

      roomsCells = [];
      
    }

    return <div className="calendar__cells__wrapper">{cells}</div>;

  }

  setCellStyle(x) {
    let style = {
      cell_style: {
        gridRowStart: x * 6 + 1, 
        gridRowEnd: (x + 1) * 6 + 1,
        border: "solid"
      }
    }
    console.log(style)
    return style;
  }

  isBooked = (room, hour) => {
    let roomHours = this.state[room];

    for (let i = 0 ;i < roomHours.length; i++) {
      if (roomHours[i] == hour) {
        return true;
      }
    }

    return false;
  }

  cellText = (room, hour) => {
    let roomHours = this.state[room];

    for (let i = 0 ;i < roomHours.length; i++) {
      if (roomHours[i] == hour) {
        return "Booked";
      }
    }

    return "";
  }

  handleClickCell = (e) => {
    let roomHours = this.state[e.target.getAttribute('data-room')];

    if (!roomHours.includes(e.target.getAttribute('data-hour'))) {
      roomHours.push(e.target.getAttribute('data-hour'));
      this.setState({[e.target.getAttribute('data-room')]:  roomHours});
    } else {
      // This is for delete or CAMPON maybe
      let filteredHours = roomHours.filter(hour => hour !== e.target.getAttribute('data-hour'))
      this.setState({[e.target.getAttribute('data-room')]: filteredHours});
    }
  }

  render() {
    return (
      <div className="calendar__container">
        {this.renderHeader()}
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
