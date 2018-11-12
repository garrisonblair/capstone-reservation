import PropTypes from 'prop-types';
import React, {Component} from 'react';
import './Calendar.scss';


class Rooms extends Component {

  state = {
    roomsList: [],
  }

  static getDerivedStateFromProps(props, state) {
    if(props.roomsList === state.roomsList) {
      return null;
    }
    return {
      roomsList: props.roomsList,
    };
  }

  render() {
    const {roomsList} = this.state;
    const rooms = roomsList.map((room) =>
      <div className="calendar__rooms__room" key={room.room_id}>
        {room.room_id}
      </div>
    );

    return <div className="calendar__rooms__wrapper">{rooms}</div>
  }
}

Rooms.propTypes = {
  roomsList: PropTypes.array,
}


export default Rooms;
