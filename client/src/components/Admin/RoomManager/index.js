import React, { Component } from 'react';
import { Button, Message, Table } from 'semantic-ui-react';
import RoomRowItem from './RoomRowItem';
import RoomModal from './RoomModal';
import api from '../../../utils/api';
import sweetAlert from 'sweetalert2';
import './RoomManager.scss';


class RoomManager extends Component {
  state = {
    roomsList: [],
    showModal: false,
    selectedRoom: null,
    showEmptyMessage: false,
  }

  componentDidMount() {
    this.syncRooms();
  }


  showRoomModal = () => {
    this.setState({
      showModal: true,
    });
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
        if (response.status === 200) {
          this.setState({
            roomsList: response.data,
            showEmptyMessage: true,
          });
        }
      })
      .catch(() => {
        sweetAlert(':(', 'We are sorry. There was a problem getting the rooms', 'error');
      });
  }

  renderRoomModal() {
    const { selectedRoom } = this.state;
    return (
      <RoomModal
        show
        onClose={this.closeRoomModal}
        selectedRoom={selectedRoom}
      />
    );
  }

  renderNoRoomList = () => {
    const { showEmptyMessage, roomsList } = this.state;
    let result = '';
    const message = (
      <Message>
        <Message.Header>There is currently no room</Message.Header>
        <p>Click on the 'Add Room' button to add a new room.</p>
      </Message>);
    if (showEmptyMessage && roomsList.length === 0) {
      result = message;
    }
    return (
      result
    );
  }

  renderTable = () => {
    const headers = ['Name', 'Capacity', '# of computers', ''];
    const { roomsList } = this.state;
    return (
      <Table>
        <Table.Header>
          <Table.Row>
            {headers.map(
              (head, index) => <Table.HeaderCell key={index} textAlign="center">{head}</Table.HeaderCell>
            )}
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {roomsList.map(
            room => (
              <RoomRowItem
                key={room.id}
                room={room}
                syncRoomList={this.syncRooms}
              />),
          )}
        </Table.Body>
      </Table>
    );
  }

  render() {
    const { showModal } = this.state;
    return (
      <div id="room-management">
        <h1>Manage Rooms</h1>
        {this.renderTable()}
        {this.renderNoRoomList()}
        <Button onClick={this.showRoomModal}>Add new room</Button>
        {showModal ? this.renderRoomModal() : ''}
      </div>
    );
  }
}

export default RoomManager;
