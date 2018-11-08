import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button, List } from 'semantic-ui-react'
import api from '../../utils/api';
import sweetAlert from 'sweetalert2';


class RoomRowItem extends Component {

  openRoomModalInEditMode =() =>{
    this.props.openModalEditMode(this.props.room);
  }

  handleDeleteRoom = () =>{
    const{room} = this.props;
    sweetAlert({
      title:'Confirmation',
      type:'warning',
      text:`Are you sure you want to delete room ${room.id}`,
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
            sweetAlert('Deleted',`Room ${room.id} was deleted.`,'success')
            .then((response)=>{
              this.props.syncRoomList();
            })
            .catch((error)=>{
              sweetAlert(':(','We are sorry. Something went wrong. Room was not deleted.', 'error')
            })
          }
        })
      }
    })
  }

  render() {
    const {id} = this.props.room;
    return (
      <List.Item className='row'>
        <List.Content floated='left'>
          <h2>Room {id}</h2>
        </List.Content>
        <List.Content floated='right' className='row-buttons'>
          <Button icon='edit' onClick={this.openRoomModalInEditMode}/>
          <Button icon='trash' onClick={this.handleDeleteRoom}/>
        </List.Content>
      </List.Item>
    )
  }
}

RoomRowItem.propTypes = {
  room: PropTypes.object.isRequired,
  syncRoomList: PropTypes.func.isRequired,
  openModalEditMode: PropTypes.func.isRequired
}

export default RoomRowItem;
