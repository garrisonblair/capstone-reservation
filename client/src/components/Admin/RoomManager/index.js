import React, { Component } from 'react';
import { Button, List, Message, Table } from 'semantic-ui-react'
import SideNav from '../SideNav';
import RoomRowItem from './RoomRowItem'
import RoomModal from './RoomModal';
import api from '../../../utils/api';
import sweetAlert from 'sweetalert2';
import './RoomManager.scss';


class RoomManager extends Component {
  state = {
    roomsList: [],
    showModal: false,
    selectedRoom: null,
    showEmptyMessage:false
  }

  componentDidMount() {
    this.syncRooms();
  }


  showRoomModal = () => {
    this.setState({
      showModal: true,
    })
  }

  closeRoomModal = () => {
    this.syncRooms();
    this.setState({
      showModal: false,
    });
  }

  syncRooms = () => {
    api.getRooms()
      .then((response) => {
        if(response.status == 200){
          this.setState({
            roomsList: response.data,
            showEmptyMessage:true
          });
        }
      })
      .catch((error)=>{
        sweetAlert(':(','We are sorry. There was a problem getting the rooms', 'error')
      })
  }

  renderRoomModal() {
    return (
      <RoomModal show={true}
        onClose={this.closeRoomModal}
        selectedRoom={this.state.selectedRoom}>
      </RoomModal>
    )
  }

  renderNoRoomList = () => {
    let {showEmptyMessage, roomsList} = this.state;
    let result = '';
    const message =
      <Message>
        <Message.Header>There is currently no room</Message.Header>
        <p>Click on the 'Add Room' button to add a new room.</p>
      </Message>;
    if(showEmptyMessage && roomsList.length == 0){
      result = message;
    }
    return (
      result
    )
  }
  renderTable = () => {
    let headers = ['Name', 'Capacity', '# of computers', '']
    return (
      <Table>
        <Table.Header>
          <Table.Row>
            {headers.map(
              (head, index) =>
                <Table.HeaderCell key={index} textAlign='center'>{head}</Table.HeaderCell>
            )}
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {this.state.roomsList.map(
            room =>
              <RoomRowItem
                key={room.id}
                room={room}
                syncRoomList={this.syncRooms}
              />
          )}
        </Table.Body>
      </Table>
    )
  }
  render() {
    let { roomsList, showModal } = this.state;
    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={'rooms'} />
          <div className="admin__content">
            <div id="room-management">
              <h1>Manage Rooms</h1>
              {this.renderTable()}
              {this.renderNoRoomList()}
              <Button onClick={this.showRoomModal}>Add new room</Button>
              {showModal ? this.renderRoomModal() : ''}
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default RoomManager;
