import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import {
  Modal, Button, FormField, Input, List, Message
} from 'semantic-ui-react';
import api from '../../utils/api';
import MemberRowItem from './MemberRowItem';
import './GroupsModal.scss';

class GroupsModal extends Component {
  state = {
    groupID: '',
    groupName: '',
    groupMembers: [],
    newMember: '',
  }

  componentDidMount() {
    console.log('me')
    const { selectedGroup } = this.props;
    if (selectedGroup != null) {
      this.setState({
        groupID: selectedGroup.id,
        groupName: selectedGroup.name,
        groupMembers: selectedGroup.members,
      });
    }
  }

  verifyModalForm = () => {
    const { groupName } = this.state;
    let result = true;
    if (groupName.length === 0) {
      sweetAlert('Empty field', 'Please enter a name.', 'warning');
      result = false;
    }
    return result;
  }

  handleNameOnChange = (event) => {
    this.setState({ groupName: event.target.value });
  }


  handleSubmit = () => {
    if (!this.verifyModalForm()) {
      return;
    }

  }

  addMemberToList = () => {
    let { groupMembers, newMember } = this.state;
    if (newMember.length < 1) {
      return;
    }
    groupMembers.push({name:newMember});
    this.setState({
      groupMembers,
      newMember: '',
    });
  }

  handleAddMemberOnChange = (e) => {
    this.setState({ newMember: e.target.value })
  }

  renderMembersList = () => {
    const { groupMembers } = this.state;
    let content = '';
    if (groupMembers.length !== 0) {
      content = (
      <List divided>
        {groupMembers.map(
          (m, index) =>
            (
              <MemberRowItem
                key={index}
                selectedMember={m.name}
              />
            ))}
      </List>
      )
    } else{
      content = (<Message visible>There is currently no members.</Message>)
    }
    return content;
  }

  render() {
    const { onClose, show, selectedGroup } = this.props;
    const { groupName, newMember} = this.state;
    return (
      <Modal centered={false} size="tiny" open={show} id="group-modal" onClose={onClose}>
        <Modal.Header>
          Group Details
        </Modal.Header>
        <Modal.Content>
          <Modal.Description>
            <h3>Group name:</h3>
            <FormField>
              <Input
                size="small"
                onChange={this.handleNameOnChange}
                value={groupName}
                readOnly={selectedGroup}
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
            {this.renderMembersList()}
            <br />
            <br />
            <Button onClick={this.handleSubmit} color="blue">SAVE</Button>

          </Modal.Description>
        </Modal.Content>
      </Modal>
    );
  }
}


export default GroupsModal;
