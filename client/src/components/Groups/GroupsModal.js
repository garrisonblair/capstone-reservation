import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import {
  Modal, Button, FormField, Input, List, Message, Dropdown,
} from 'semantic-ui-react';
import api from '../../utils/api';
import MemberRowItem from './MemberRowItem';
import './GroupsModal.scss';

class GroupsModal extends Component {
  state = {
    groupId: '',
    groupOwner: '',
    groupName: '',
    groupMembers: [],
    cleanGroupMembers: [],
    newMembers: [],
    deletedMembers: [],
    newMember: '',
    stateOptions: [],
    bookers: [],
  }

  componentDidMount() {
    const { selectedGroup } = this.props;
    let newStateOptions = [];

    if (selectedGroup !== null) {
      const tempGroupMembers = [];
      selectedGroup.members.map(m => tempGroupMembers.push(m.user.id));
      this.setState({
        groupId: selectedGroup.id,
        groupOwner: selectedGroup.owner.user,
        groupName: selectedGroup.name,
        groupMembers: tempGroupMembers,
        cleanGroupMembers: tempGroupMembers,
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
        r2.data.map(b => newStateOptions.push({
          key: b.id, value: b.user.id, text: b.user.username,
        }));
        if (selectedGroup !== null) {
          selectedGroup.members
            .filter(m => m.user.id !== selectedGroup.owner.user.id)
            .forEach((m) => {
              newStateOptions = newStateOptions.filter(o => o.value !== m.user.id);
            });
        }
        this.setState({
          stateOptions: newStateOptions,
          bookers: r2.data,
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
      newMember, newMembers, groupOwner, groupMembers,
      cleanGroupMembers, deletedMembers, stateOptions,
    } = this.state;
    if (newMember.length < 1) {
      return;
    }
    if (newMember === groupOwner.id) {
      sweetAlert('Info', 'Cannot add yourself. You are already part of the group.', 'warning');
      return;
    }
    if (cleanGroupMembers.includes(newMember) && deletedMembers.includes(newMember)) {
      this.setState({
        deletedMembers: deletedMembers.filter(m => m !== newMember),
        groupMembers: groupMembers.concat([newMember]),
      });
    } else {
      newMembers.push(newMember);
      this.setState({
        newMembers,
        newMember: '',
      });
    }
    this.setState({ stateOptions: stateOptions.filter(o => o.value !== newMember) });
  }

  handleDropboxChange = (e, { value }) => {
    this.setState({ newMember: value });
  }

  deleteFunction = (member) => {
    const {
      groupMembers, newMembers, deletedMembers, bookers, stateOptions,
    } = this.state;

    if (groupMembers.includes(member)) {
      this.setState({
        groupMembers: groupMembers.filter(m => m !== member),
        deletedMembers: deletedMembers.concat([member]),
      });
    } else if (newMembers.includes(member)) {
      this.setState({ newMembers: newMembers.filter(m => m !== member) });
    }
    const m = bookers.find(b => b.user.id === member);
    stateOptions.push({ key: m.user.id, value: m.user.id, text: m.user.username });
    this.setState({ stateOptions });
  }

  handleSubmit = () => {
    const {
      groupName, newMembers, groupId, deletedMembers,
    } = this.state;
    const { onClose } = this.props;
    if (!this.verifyModalForm()) {
      return;
    }
    if (groupId === '') {
      api.createGroup(groupName)
        .then((r) => {
          if (r.status === 201) {
            api.addMembersToGroup(r.data.id, newMembers)
              .then((r2) => {
                if (r2.status === 202) {
                  sweetAlert('Completed', 'A group was created.', 'success');
                  onClose();
                }
              });
          }
        });
    } else {
      if (newMembers.length === 0 && deletedMembers.length === 0) {
        sweetAlert('Completed', 'Group was saved.', 'success');
        return;
      }
      if (newMembers.length !== 0) {
        api.addMembersToGroup(groupId, newMembers)
          .then((r) => {
            if (r.status === 202 && deletedMembers.length === 0) {
              sweetAlert('Completed', 'Group was saved.', 'success');
              onClose();
            }
          })
          .catch((error) => {
            sweetAlert('Error', JSON.stringify(error), 'error');
          });
      }

      if (deletedMembers.length !== 0) {
        api.removeMembersToGroup(groupId, deletedMembers)
          .then((r) => {
            if (r.status === 202) {
              sweetAlert('Completed', 'Group was saved.', 'success');
              onClose();
            }
          })
          .catch((error) => {
            sweetAlert('Error', JSON.stringify(error), 'error');
          });
      }
    }
  }

  renderMembersList = () => {
    const {
      groupMembers, newMembers, groupOwner, bookers,
    } = this.state;
    const { isAdmin } = this.props;
    const list = groupMembers.concat(newMembers);
    let content = (
      <List divided>
        {
          list.filter(w => w !== groupOwner.id).map(
            (m) => {
              const user = bookers.find(b => b.user.id === m);
              return user !== undefined ? (
                <MemberRowItem
                  key={m}
                  selectedMember={user}
                  deleteFunction={this.deleteFunction}
                  isAdmin={isAdmin}
                />
              ) : '';
            },
          )}
      </List>
    );

    if (groupMembers.length === 0 && newMembers.length === 0) {
      content = (<Message visible>There is currently no members except you.</Message>);
    }
    return content;
  }

  render() {
    const {
      onClose, show, selectedGroup, isAdmin,
    } = this.props;
    const {
      groupName, groupOwner, stateOptions, newMember,
    } = this.state;
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
            <h3>
              Group Owner:
              {groupOwner.username}
            </h3>
            <h3>Members:</h3>
            <FormField>
              <Dropdown
                placeholder="New member"
                search
                selection
                options={stateOptions}
                onChange={this.handleDropboxChange}
                value={newMember}
              />
              <Button onClick={this.addMemberToList}>Add member</Button>
            </FormField>
            {this.renderMembersList()}
            <br />
            <br />
            <Button onClick={this.handleSubmit} color="blue">SAVE</Button>
            <Button color="red" onClick={isAdmin ? this.handleDeleteGroup : this.handleLeaveGroup}>
              {isAdmin ? 'Delete group' : 'Leave group'}
            </Button>
          </Modal.Description>
        </Modal.Content>
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
