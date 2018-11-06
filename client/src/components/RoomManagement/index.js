import React, { Component } from 'react';
import './RoomManagement.scss';
import { Button, List } from 'semantic-ui-react'
import RoomRowItem from './RoomRowItem'

class RoomManagement extends Component {
  state = {
    roomsList: [],
    addNewToogle: false
  }

  componentWillMount(){
    this.setState({
      roomsList:[
        { id:1,capacity:2, numComputers:1 },
        { id:2,capacity:2, numComputers:1 },
        { id:3,capacity:2, numComputers:1 },
        { id:4,capacity:2, numComputers:1 },
        { id:5,capacity:2, numComputers:1 }
      ]
    })

  }
  showRoomModal = () =>{

  }

  render() {
    let { roomsList } = this.state;

    return (
      <div id="room-management">
        <h1>Manage Rooms</h1>
        <List divided verticalAlign='middle'>
          {roomsList.map(room => <RoomRowItem key={room.id} room={room} />)}
        </List>
        <Button onClick={this.showRoomModal}>Add new room</Button>
      </div>
    )
  }
}

export default RoomManagement;
