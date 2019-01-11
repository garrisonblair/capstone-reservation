import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import {
  Modal, Button, FormField, Input, List, Dropdown,
} from 'semantic-ui-react';
import api from '../../utils/api';
import './GroupsModal.scss';
import MemberRowItem from './MemberRowItem';

class GroupsModal extends Component {
  state = {
    groupId: '',
    groupOwner: '',
    groupName: '',
    groupInvitations: [],
    newInvitations: [],
    // deletedInvitations: [],
    newInvitation: '',
    stateOptions: [],
  }

  componentDidMount() {
    const { selectedGroup } = this.props;
    const { stateOptions } = this.state;

    if (selectedGroup !== null) {
      this.setState({
        groupId: selectedGroup.id,
        groupOwner: selectedGroup.owner.user,
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
    api.getBookers()
      .then((r2) => {
        r2.data.map(b => stateOptions.push({
          key: b.user.id, value: b.user.id, text: b.user.username,
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
      newInvitation, groupId, groupInvitations, groupOwner,
    } = this.state;
    if (groupInvitations.some(i => i.invited_booker.user.id === newInvitation)) {
      sweetAlert('Warning', 'You already invited that user.', 'warning');
      return;
    }
    if (groupOwner.id === newInvitation) {
      sweetAlert('Warning', 'Cannot invite yourself', 'warning');
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
          sweetAlert('Completed', 'You left the group.', 'success');
        }
      });
  }

  deleteFunction = (invitationId) => {
    let { groupInvitations } = this.state;
    api.revokeInvitation(invitationId)
      .then((r) => {
        if (r.status === 200) {
          groupInvitations = groupInvitations.filter(i => i.id !== invitationId);
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
          this.setState({ groupId: r.data.id });
        }
      });
  }

  renderMembersList = () => {
    const {
      groupInvitations, newInvitations,
    } = this.state;
    const { isAdmin } = this.props;
    let content = (
      <div>
        <h3>Invitation List:</h3>
        <List divided>
          {
            groupInvitations.map(i => (
              <MemberRowItem
                key={i.id}
                selectedInvitation={i}
                deleteFunction={this.deleteFunction}
                isAdmin={isAdmin}
              />
            ))
          }
        </List>
      </div>
    );

    if (groupInvitations.length === 0 && newInvitations.length === 0) {
      // content = (<Message visible>There is currently no members except you.</Message>);
      content = '';
    }
    return content;
  }

  renderRedButton = () => {
    const { isAdmin } = this.props;
    const { groupId } = this.state;
    let button = '';
    if (groupId === '') {
      return '';
    }
    if (isAdmin === true) {
      button = <Button onClick={this.handleDeleteGroup} color="red">Delete Group</Button>;
    } else if (isAdmin === false) {
      button = <Button onClick={this.handleLeaveGroup} color="red">Leave Group</Button>;
    }

    return (button);
  }

  renderModalContent = () => {
    const {
      groupOwner, stateOptions, newInvitation,
    } = this.state;
    return (
      <Modal.Content>
        <Modal.Description>
          <h3>
            Group Owner:
            {groupOwner.username}
          </h3>

          <FormField>
            <Dropdown
              placeholder="Users"
              selection
              options={stateOptions}
              onChange={this.handleDropboxChange}
              value={newInvitation}
            />
            <Button onClick={this.addMemberToList}>Invite</Button>
          </FormField>
          <br />
          {this.renderMembersList()}
          <br />
          <br />
          {this.renderRedButton()}
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
          {groupId === '' ? <Button onClick={this.handleCreateGroup}>Create group</Button> : ''}
        </Modal.Header>
        {groupId !== '' ? this.renderModalContent() : ''}
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
  isAdmin: PropTypes.bool,
};

GroupsModal.defaultProps = {
  selectedGroup: null,
  isAdmin: false,
};


export default GroupsModal;
