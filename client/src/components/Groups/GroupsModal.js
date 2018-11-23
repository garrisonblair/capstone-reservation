import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import {
  Modal, Button, FormField, Input, List,
} from 'semantic-ui-react';
import api from '../../utils/api';
import MemberRowItem from './MemberRowItem';
import './GroupsModal.scss';

class GroupsModal extends Component {
  state = {
    groupID: '',
    groupName: '',
    groupMembers: [],
    newMember: ''
  }

  componentDidMount() {
    // const { selectedRoom } = this.props;
    // if (selectedRoom != null) {
    //   this.setState({
    //     roomID: selectedRoom.name,
    //     roomCapacity: selectedRoom.capacity,
    //     numOfComputers: selectedRoom.number_of_computers,
    //   });
    // }
  }

  verifyModalForm = () => {

  }

  handleGroupIdOnChange = (event) => {
    // this.setState({ groupID: event.target.value });
  }


  handleSubmit = () => {

  }

  addMemberToList = () => {
    let { groupMembers, newMember } = this.state;
    groupMembers.push(newMember);
    this.setState({
      groupMembers,
      newMember:'',
    });
  }
  handleAddMemberOnChange = (e) => {
    this.setState({ newMember: e.target.value })
  }

  render() {
    const { onClose } = this.props;
    const { groupID, selectedGroup, newMember, groupMembers } = this.state;
    console.log(groupMembers);
    return (
      <Modal centered={false} size="tiny" open={true} id="group-modal" onClose={onClose}>
        <Modal.Header>
          Group Details
        </Modal.Header>
        <Modal.Content>
          <Modal.Description>
            <h3>Group name:</h3>
            <FormField>
              <Input
                size="small"
                onChange={this.handleGroupIdOnChange}
                value={groupID}
                disabled={selectedGroup != null}
              />
            </FormField>
            <h3>Members:</h3>
            <FormField>
              <Input
                size="small"
                action={<Button content='Add' onClick={this.addMemberToList} />}
                onChange={this.handleAddMemberOnChange}
                placeholder='Add members'
                value={newMember}
              />
            </FormField>
            <List divided>
              {groupMembers.map(
                m =>
                  (
                    <MemberRowItem
                      selectedMember={m}
                    />
                  ))}
            </List>
            <br />
            <br />
            <Button onClick={this.handleSubmit} color="blue">SAVE</Button>
            <Button onClick={onClose}>Close</Button>
          </Modal.Description>
        </Modal.Content>
      </Modal>
    );
  }
}


export default GroupsModal;
