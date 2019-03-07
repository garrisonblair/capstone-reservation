import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import {
  Modal, Button, FormField, Input, List, Loader, Dimmer,
} from 'semantic-ui-react';
import api from '../../utils/api';
import storage from '../../utils/local-storage';
import InvitedRowItem from './InvitedRowItem';
import MemberRowItem from './MemberRowItem';
import RequestPrivilege from './RequestPrivilege';
import './GroupsModal.scss';
import UserSearch from '../ReusableComponents/UserSearch';

class GroupsModal extends Component {
  state = {
    groupId: '',
    groupOwner: '',
    groupName: '',
    groupInvitations: [],
    groupMembers: [],
    newInvitations: [],
    newInvitation: '',
    groupPrivilegeRequest: null,
    isLoading: false,
  }

  componentDidMount() {
    const { selectedGroup } = this.props;
    if (selectedGroup !== null) {
      this.setState({
        groupId: selectedGroup.id,
        groupOwner: selectedGroup.owner,
        groupMembers: selectedGroup.members,
        groupName: selectedGroup.name,
        groupInvitations: selectedGroup.group_invitations,
        groupPrivilegeRequest: selectedGroup.privilege_request,
      });
    } else {
      api.getUser(storage.getUser().id)
        .then((r) => {
          this.setState({ groupOwner: r.data });
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
    this.setState({ isLoading: true });
    api.inviteMembers(groupId, [newInvitation])
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 201) {
          groupInvitations.push(r.data[0]);
          this.setState({
            groupInvitations,
          });
        }
      })
      .catch((r) => {
        if (r.response.status === 401) {
          this.setState({ isLoading: false });
          sweetAlert.fire({
            position: 'top',
            type: 'error',
            title: 'Cannot Invite Member',
            text: r.response.data,
          });
        } else {
          sweetAlert(':(', 'Something went wrong. Please refresh.', 'error');
          this.setState({ isLoading: false });
          // eslint-disable-next-line no-console
          console.log(r);
        }
      });
  }

  handleDropboxChange = (user) => {
    if (user === null) {
      this.setState({ newInvitation: '' });
    } else {
      this.setState({ newInvitation: user.id });
    }
  }

  handleLeaveGroup = () => {
    this.setState({ isLoading: true });
    const { groupId } = this.state;
    const { onClose } = this.props;
    api.leaveGroup(groupId)
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 202) {
          onClose();
          sweetAlert('Completed', 'You have left the group.', 'success');
        }
      });
  }

  handleDeleteGroup = () => {
    this.setState({ isLoading: true });
    const { groupId } = this.state;
    const { onClose } = this.props;
    api.leaveGroup(groupId)
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 202) {
          onClose();
          sweetAlert('Completed', 'You have deleted the group.', 'success');
        }
      });
  }

  deleteInvitation = (invitationId) => {
    // this.setState({ isLoading: true });
    const { groupInvitations } = this.state;
    api.revokeInvitation(invitationId)
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 200) {
          this.setState({ groupInvitations: groupInvitations.filter(i => i.id !== invitationId) });
        }
      });
  }

  deleteMember = (memberId) => {
    this.setState({ isLoading: true });
    const { groupId, groupMembers } = this.state;
    api.removeMembersFromGroup(groupId, [memberId])
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 202) {
          this.setState({ groupMembers: groupMembers.filter(m => m.id !== memberId) });
        }
      });
  }

  handleCreateGroup = () => {
    this.setState({ isLoading: true });
    if (!this.verifyModalForm()) {
      return;
    }
    const { groupName } = this.state;
    api.createGroup(groupName)
      .then((r) => {
        this.setState({ isLoading: false });
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
    const { groupMembers } = this.state;
    const { isAdmin } = this.props;

    const content = (
      <List divided>
        {
          groupMembers.map(
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
    return content;
  }

  renderModalContent = () => {
    const {
      groupId, groupPrivilegeRequest,
    } = this.state;
    const { isAdmin } = this.props;
    return (
      <Modal.Content>
        <Modal.Description>
          <FormField>
            <RequestPrivilege groupId={groupId} groupPrivilege={groupPrivilegeRequest} />
            <h3>
              Members:
            </h3>
            {isAdmin ? (
              <div>
                <UserSearch maxUsers={4} onSelect={this.handleDropboxChange} />
                <Button onClick={this.addMemberToList} className="button-right">Invite</Button>
              </div>
            ) : ''
            }
          </FormField>
          {this.renderMembersList()}
          <br />
          {this.renderInvitedList()}
        </Modal.Description>
      </Modal.Content>
    );
  }

  render() {
    const { onClose, show, selectedGroup } = this.props;
    const { groupId, groupName, isLoading } = this.state;
    return (
      <Modal centered={false} size="tiny" open={show} id="groups-modal" onClose={onClose}>
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
        <Dimmer active={isLoading} inverted>
          <Loader />
        </Dimmer>
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
