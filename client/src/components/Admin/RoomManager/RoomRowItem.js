import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button, Table } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import RoomModal from './RoomModal';


class RoomRowItem extends Component {
  state = {
    openModal: false,
  }

  openModal = () => {
    this.setState({ openModal: true });
  }

  closeModal = () => {
    const { syncRoomList } = this.props;
    syncRoomList();
    this.setState({ openModal: false });
  }

  handleDeleteRoom = () => {
    const { room, syncRoomList } = this.props;
    sweetAlert({
      title: 'Confirmation',
      type: 'warning',
      text: `Are you sure you want to delete room ${room.name}`,
      showConfirmButton: true,
      confirmButtonText: 'Delete',
      showCancelButton: true,
      cancelButtonText: 'Cancel',
      confirmButtonColor: 'red',
    })
      .then((result) => {
        if (result.value) {
          api.deleteRoom(room.id)
            .then((response) => {
              if (response.status) {
                sweetAlert('Deleted', `Room '${room.name}' was deleted.`, 'success')
                  .then(() => {
                    syncRoomList();
                  });
              }
            })
            .catch(() => {
              sweetAlert(':(', 'We are sorry. Something went wrong. Room was not deleted.', 'error');
            });
        }
      });
  }

  render() {
    const { room } = this.props;
    const { openModal } = this.state;
    return (
      <Table.Row key={room.id}>
        <Table.Cell textAlign="center"><h4>{room.name}</h4></Table.Cell>
        <Table.Cell textAlign="center">{room.capacity}</Table.Cell>
        <Table.Cell textAlign="center">{room.number_of_computers}</Table.Cell>
        <Table.Cell textAlign="center">
          <Button icon="edit" onClick={this.openModal} />
          <Button icon="trash" onClick={this.handleDeleteRoom} />
        </Table.Cell>
        <RoomModal
          show={openModal}
          selectedRoom={room}
          onClose={this.closeModal}
        />
      </Table.Row>
    );
  }
}

RoomRowItem.propTypes = {
  room: PropTypes.shape({
    id: PropTypes.number.isRequired,
    capacity: PropTypes.number.isRequired,
    number_of_computers: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
  }).isRequired,
  syncRoomList: PropTypes.func.isRequired,
};

export default RoomRowItem;
