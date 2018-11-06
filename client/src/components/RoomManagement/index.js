import React, { Component } from 'react';
import './RoomManagement.scss';
import { Button, List, Modal} from 'semantic-ui-react'
import RoomRowItem from './RoomRowItem'
import RoomModal from './RoomModal';

class RoomManagement extends Component {
  state = {
    roomsList: [],
    showModal:false
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
    this.setState({ showModal:true })
  }
  closeRoomModal = () =>{
    this.setState({ showModal:false })
  }

  render() {
    let { roomsList, showModal} = this.state;
    console.log(this.state.showModal)
    return (
      <div id="room-management">
        <h1>Manage Rooms</h1>
        <List divided verticalAlign='middle'>
          {roomsList.map(room => <RoomRowItem key={room.id} room={room} />)}
        </List>
        <Button onClick={this.showRoomModal}>Add new room</Button>
        <RoomModal show={showModal} closeModal={this.closeRoomModal}></RoomModal>

      </div>
    )
  }
}

export default RoomManagement;
