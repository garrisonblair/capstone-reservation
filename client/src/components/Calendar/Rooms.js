import React, { Component } from 'react';
import './Calendar.scss';


class Rooms extends Component {
  state = {
    roomsList: [],
    roomsNum: 0,
    orientation: 0,
  }

  static getDerivedStateFromProps(props, state) {
    if (props.roomsList === state.roomsList && props.orientation === state.orientation) {
      return null;
    }
    return {
      roomsList: props.roomsList,
      roomsNum: props.roomsNum,
      orientation: props.orientation,
    };
  }

  setStyle() {
    const { roomsNum, orientation } = this.state;
    let style;
    if (orientation === 0) {
      style = {
        gridTemplateColumns: `repeat(${roomsNum}, 1fr)`,
        gridColumnStart: 2,
      };
    } else {
      style = {
        gridTemplateRows: `repeat(${roomsNum}, 1fr)`,
      };
    }
    return style;
  }

  render() {
    const { roomsList } = this.state;
    const rooms = roomsList.map(room => (
      <div className="calendar__rooms__room" key={room.name}>
        {room.name}
      </div>
    ));

    return <div className="calendar__rooms__wrapper" style={this.setStyle()}>{rooms}</div>;
  }
}

export default Rooms;
