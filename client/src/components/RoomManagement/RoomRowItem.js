import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button, List } from 'semantic-ui-react'
import sweetAlert from 'sweetalert2';


class RoomRowItem extends Component {

  handleDeleteRoom = () =>{
    const{room} = this.props;
    sweetAlert({
      title:'',
      type:'warning',
      text:`Are you sure you want to delete room ${room.id}`,
      showConfirmButton:true,
      confirmButtonText:'Delete',
      showCancelButton:true,
      cancelButtonText:'Cancel',
      cancelButtonColor:'red'
    })
    .then((result)=>{
      if(result.value){
        //axios delete
        sweetAlert('Deleted',`Room ${room.id} was deleted.`,'success')
        .then((response)=>{
          this.props.actionWhenSuccess();
        });
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
          <Button icon='edit'/>
          <Button icon='trash' onClick={this.handleDeleteRoom}/>
        </List.Content>
      </List.Item>
    )
  }
}

RoomRowItem.propTypes = {
  room: PropTypes.object.isRequired,
  actionWhenSuccess: PropTypes.func.isRequired
}

export default RoomRowItem;
