import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button, List , Table} from 'semantic-ui-react'
import api from '../../../utils/api';
import RoomModal from './RoomModal';
import sweetAlert from 'sweetalert2';


class RoomRowItem extends Component {

  state={
    openModal:false
  }
  openModal = () =>{
    console.log('opened');
    this.setState({openModal:true})
  }
  closeModal = () =>{
    this.props.syncRoomList();
    this.setState({openModal:false})
  }
  handleDeleteRoom = () =>{
    const{room} = this.props;
    sweetAlert({
      title:'Confirmation',
      type:'warning',
      text:`Are you sure you want to delete room ${room.room_id}`,
      showConfirmButton:true,
      confirmButtonText:'Delete',
      showCancelButton:true,
      cancelButtonText:'Cancel',
      confirmButtonColor:'red'
    })
    .then((result)=>{
      if(result.value){
        api.deleteRoom(room.id)
        .then((response) =>{
          if(response.status){
            sweetAlert('Deleted',`Room ${room.room_id} was deleted.`,'success')
            .then((response)=>{
              this.props.syncRoomList();
            })
          }
        })
        .catch((error)=>{
          sweetAlert(':(','We are sorry. Something went wrong. Room was not deleted.', 'error')
        })
      }
    })
  }

  render() {
    const {id,room_id, capacity, number_of_computers} = this.props.room;
    return (
      <Table.Row key={id}>
        <Table.Cell  textAlign='center'><h4>{room_id}</h4></Table.Cell>
        <Table.Cell textAlign='center'>{capacity}</Table.Cell>
        <Table.Cell textAlign='center'>{number_of_computers}</Table.Cell>
        <Table.Cell textAlign='center'>
          <Button icon='edit' onClick={this.openModal}/>
          <Button icon='trash' onClick={this.handleDeleteRoom}/></Table.Cell>
           <RoomModal
             show={this.state.openModal}
             selectedRoom={this.props.room}
             onClose={this.closeModal}/>
      </Table.Row>
    )
  }
}

RoomRowItem.propTypes = {
  room: PropTypes.object.isRequired,
  syncRoomList: PropTypes.func.isRequired
}

export default RoomRowItem;
