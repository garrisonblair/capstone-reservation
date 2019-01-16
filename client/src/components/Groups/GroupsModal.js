import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import {
  Modal, Button, FormField, Input, List, Dropdown, Message,
} from 'semantic-ui-react';
import api from '../../utils/api';
import InvitedRowItem from './InvitedRowItem';
import MemberRowItem from './MemberRowItem';

class GroupsModal extends Component {
  state = {
    groupId: '',
    groupOwner: '',
    groupName: '',
    groupInvitations: [],
    groupMembers: [],
    newInvitations: [],
    newInvitation: '',
    stateOptions: [],
  }

  componentDidMount() {
    const { selectedGroup } = this.props;
    const { stateOptions } = this.state;
    if (selectedGroup !== null) {
      this.setState({
        groupId: selectedGroup.id,
        groupOwner: selectedGroup.owner,
        groupMembers: selectedGroup.members,
        groupName: selectedGroup.name,
        groupInvitations: selectedGroup.group_invitations,
      });
    } else {
      api.getMyUser()
        .then((r) => {
          this.setState({ groupOwner: r.data });
        });
    }

    // get all users and add them to the dropbox
    api.getUsers()
      .then((r2) => {
        r2.data.map(b => stateOptions.push({
          key: b.id, value: b.id, text: b.username,
        }));
        this.setState({
          stateOptions,
        });
      });
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

  addMemberToList = () => {
    const {
      newInvitation, groupId, groupInvitations, groupOwner, groupMembers,
    } = this.state;
    if (groupInvitations.some(i => i.invited_booker.id === newInvitation)) {
      sweetAlert('Warning', 'You already invited that user.', 'warning');
      return;
    }
    if (groupMembers.some(m => m.id === newInvitation)) {
      sweetAlert('Warning', 'User is already a member.', 'warning');
      return;
    }
    if (groupOwner.id === newInvitation) {
      sweetAlert('Warning', 'Cannot invite yourself.', 'warning');
      return;
    }
    api.inviteMembers(groupId, [newInvitation])
      .then((r) => {
        if (r.status === 201) {
          groupInvitations.push(r.data[0]);
          this.setState({
            groupInvitations,
          });
        }
      });
  }

  handleDropboxChange = (e, { value }) => {
    this.setState({ newInvitation: value });
  }

  handleLeaveGroup = () => {
    const { groupId } = this.state;
    const { onClose } = this.props;
    api.leaveGroup(groupId)
      .then((r) => {
        if (r.status === 202) {
          onClose();
          sweetAlert('Completed', 'You have left the group.', 'success');
        }
      });
  }

  handleDeleteGroup = () => {
    const { groupId } = this.state;
    const { onClose } = this.props;
    api.leaveGroup(groupId)
      .then((r) => {
        if (r.status === 202) {
          onClose();
          sweetAlert('Completed', 'You have deleted the group.', 'success');
        }
      });
  }

  deleteInvitation = (invitationId) => {
    const { groupInvitations } = this.state;
    api.revokeInvitation(invitationId)
      .then((r) => {
        if (r.status === 200) {
          this.setState({ groupInvitations: groupInvitations.filter(i => i.id !== invitationId) });
        }
      });
  }

  deleteMember = (memberId) => {
    const { groupId, groupMembers } = this.state;
    api.removeMembersFromGroup(groupId, [memberId])
      .then((r) => {
        if (r.status === 202) {
          this.setState({ groupMembers: groupMembers.filter(m => m.id !== memberId) });
        }
      });
  }

  handleCreateGroup = () => {
    if (!this.verifyModalForm()) {
      return;
    }
    const { groupName } = this.state;
    api.createGroup(groupName)
      .then((r) => {
        if (r.status === 201) {
          this.setState({
            groupId: r.data.id,
            groupMembers: r.data.members,
          });
        }
      });
  }

  renderInvitedList = () => {
    const {
      groupInvitations, newInvitations,
    } = this.state;
    const { isAdmin } = this.props;
    let content = (
      <div>
        <h3>Invitation:</h3>
        <List divided>
          {
            groupInvitations.map(i => (
              <InvitedRowItem
                key={i.id}
                selectedInvitation={i}
                deleteFunction={this.deleteInvitation}
                isAdmin={isAdmin}
              />
            ))
          }
        </List>
      </div>
    );

    if (groupInvitations.length === 0 && newInvitations.length === 0) {
      content = '';
    }
    return content;
  }

  renderRedButton = () => {
    const { isAdmin } = this.props;
    const { groupId } = this.state;
    let button = '';
    if (groupId === '') {
      button = '';
    } else if (isAdmin === true) {
      button = <Button onClick={this.handleDeleteGroup} color="red">Delete Group</Button>;
    } else if (isAdmin === false) {
      button = <Button onClick={this.handleLeaveGroup} color="red">Leave Group</Button>;
    }
    return (button);
  }

  renderMembersList = () => {
    const { groupMembers, groupOwner } = this.state;
    const { isAdmin } = this.props;

    let content = (
      <List divided>
        {
          groupMembers.filter(m => m.id !== groupOwner.id).map(
            m => (
              <MemberRowItem
                member={m}
                deleteFunction={this.deleteMember}
                key={m.id}
                isAdmin={isAdmin}
              />
            ),
          )
        }
      </List>
    );
    if (groupMembers.length === 1) {
      content = (<Message visible>There is currently no members except you.</Message>);
    }
    return content;
  }

  renderModalContent = () => {
    const {
      groupOwner, stateOptions, newInvitation,
    } = this.state;
    const { isAdmin } = this.props;
    return (
      <Modal.Content>
        <Modal.Description>
          <h3>
            Group Owner:
            {groupOwner.username}
          </h3>
          <FormField>
            {isAdmin ? (
              <div>
                <Dropdown
                  placeholder="Users"
                  selection
                  options={stateOptions}
                  onChange={this.handleDropboxChange}
                  value={newInvitation}
                />
                <Button onClick={this.addMemberToList}>Invite</Button>
              </div>) : ''
            }

          </FormField>
          <br />
          <h3>Members:</h3>
          {this.renderMembersList()}
          <br />
          {this.renderInvitedList()}
        </Modal.Description>
      </Modal.Content>
    );
  }

  render() {
    const { onClose, show, selectedGroup } = this.props;
    const { groupId, groupName } = this.state;
    return (
      <Modal centered={false} size="tiny" open={show} id="group-modal" onClose={onClose}>
        <Modal.Header>
          <Input
            size="small"
            onChange={this.handleNameOnChange}
            placeholder="Group's name"
            value={groupName}
            readOnly={selectedGroup}
          />
          {groupId === '' ? <Button onClick={this.handleCreateGroup} color="blue">Create group</Button> : ''}
        </Modal.Header>
        {groupId !== '' ? this.renderModalContent() : ''}
        <Modal.Actions>
          <Button onClick={onClose}>Cancel</Button>
          {this.renderRedButton()}
        </Modal.Actions>
      </Modal>
    );
  }
}

GroupsModal.propTypes = {
  onClose: PropTypes.func.isRequired,
  show: PropTypes.bool.isRequired,
  selectedGroup: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    is_verified: PropTypes.bool.isRequired,
    owner: PropTypes.object.isRequired,
    privilege_category: PropTypes.number,
    members: PropTypes.array.isRequired,
  }),
  isAdmin: PropTypes.bool.isRequired,
};

GroupsModal.defaultProps = {
  selectedGroup: null,
};


export default GroupsModal;