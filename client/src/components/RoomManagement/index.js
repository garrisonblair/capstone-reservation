import React, { Component } from 'react';
import './RoomManagement.scss';
import { Button, Image, List } from 'semantic-ui-react'

class RoomManagement extends Component {
  state = {
    roomsList:[]
  }

  render() {
    return (
      <div id="room-management">
        <h1>Manage Rooms</h1>
        <Button>Add new room</Button>
      </div>
    )
  }
}

export default RoomManagement;
