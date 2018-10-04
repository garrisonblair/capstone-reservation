import React, {Component} from 'react';
import settings from '../../config/settings';
import './Calendar.scss';


class Calendar extends Component {
  
  state = {
    roomsList: [1,2,3,4,5,6,7,8,9,10],
    dateSelected: new Date(),
    hourStart: 8,
    hourEnd: 23,
    hourIncrement: 1
  };

  componentDidMount() {
    console.log(settings)
  }

  renderHeader() {
    return (
      <div className="header row flex-middle">
        {/* <div className="col col-start">
          <div className="icon" onClick={this.prevMonth}>
            chevron_left
          </div>
        </div> */}
        <div className="col col-center">
          <span>
            {this.state.dateSelected.toDateString()}
          </span>
        </div>
        {/* <div className="col col-end" onClick={this.nextMonth}>
          <div className="icon">chevron_right</div>
        </div> */}
      </div>
    );
  }

  renderRooms() {
    const { roomsList } = this.state;
    const rooms = roomsList.map((room) =>
      <div className="col col-center" key={room}>
        {room}
      </div>
    );
    
    return <div className="calendar__rooms row">{rooms}</div>
  }

  renderHours() {
    const { hourStart, hourEnd, hourIncrement } = this.state;
    const hours = [];

    for (let hour = hourStart; hour <= hourEnd; hour += hourIncrement) {
      hours.push(
        <div className="calendar__hours--label" key={hour}>
          {hour}
        </div>
      )
    }

    return <div className="calendar__hours">{hours}</div>
  }

  renderCells() {
    const { hourStart, hourEnd, hourIncrement } = this.state;
    const { roomsList } = this.state;

    let cells = [];
    let rows = [];
    let numberOfRows = (hourEnd - hourStart + 1) / hourIncrement;
    let numberOfCells = numberOfRows * (roomsList.length);
    let cell = 0;

    while (cell < numberOfCells) {
      for (let j = 0; j < roomsList.length; j++) {
        cells.push(
          <div className={`calendar__cells__cell-${j} ${
            this.isBooked(currentRoom, currentHour)
              ? "booked"
              : ""
          }`} style={this.setCellStyle(j).cell_style} key={cell} data-hour={currentHour} data-room={currentRoom} onClick={this.handleClickCell}>{this.cellText(currentRoom, currentHour)}</div>
        );
        cell++;
      }
      
      rows.push(
        <div className="row" key={cell}>
          {cells}
        </div>
      )
      cells = [];
    }

    return <div className="body">{rows}</div>;

  }

  handleClickCell(e) {
    alert(e.target.getAttribute('data-key'));
  }
  // schedules() {
  //   axios({
  //     method: 'GET',
  //     url: `${settings.API_ROOT}/videoframes`,
  //    })
  //    .then((response) => {
  //      const schedules = response.data.map(schedule => schedule);
  //      this.setState({schedule});
  //    })
  //    .catch(error => {
  //     console.log(error);
  //     const errorMsg = "Oops, something went wrong while fetching items!";
  //     this.setState({errorMsg});
  //   })
  // }

  render() {
    return (
      <div className="calendar">
        {this.renderHeader()}
        {this.renderRooms()}
        {/* {this.renderHours()} */}
        {this.renderCells()}   
      </div>
    )
  }
}

export default Calendar;
