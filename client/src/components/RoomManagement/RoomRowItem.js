import React, { Component } from 'react';
import { Button, List, Icon } from 'semantic-ui-react'


class RoomRowItem extends Component {

  handleDeleteRoom = () =>{

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

export default RoomRowItem;
