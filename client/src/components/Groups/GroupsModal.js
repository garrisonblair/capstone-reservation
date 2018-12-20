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
    newMembers: [],
    deletedMembers: [],
    newMember: '',
    stateOptions: [],
  }

  componentDidMount() {
    const { selectedGroup } = this.props;
    const newStateOptions = [];

    if (selectedGroup !== null) {
      const tempGroupMembers = [];
      selectedGroup.members.map(m => tempGroupMembers.push(m.user.username));
      this.setState({
        groupId: selectedGroup.id,
        groupOwner: selectedGroup.owner.user.username,
        groupName: selectedGroup.name,
        groupMembers: tempGroupMembers,
      });
    } else {
      api.getMyUser()
        .then((r) => {
          this.setState({ groupOwner: r.data.username });
          // get all users and add them to the dropbox
        });
    }
    api.getUsers()
      .then((r2) => {
        r2.data.filter(u => u.is_superuser === false)
          .map(u => newStateOptions.push({
            key: u.username, value: u.username, text: u.username,
          }));
        this.setState({ stateOptions: newStateOptions });
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

  handleSubmit = () => {
    const { groupName, newMembers, groupId } = this.state;
    const { onClose } = this.props;
    if (!this.verifyModalForm()) {
      return;
    }
    if (groupId === '') {
      api.createGroup(groupName, newMembers)
        .then((r) => {
          if (r.status === 201) {
            sweetAlert('Completed', 'A group was created.', 'success')
              .then(() => {
                onClose();
              });
          }
        });
    } else {
      api.addMembersToGroup(groupId, newMembers)
        .then((r) => {
          if (r.status === 202) {
            sweetAlert('Completed', `Group #${groupId} was modified.`, 'success')
              .then(() => {
                onClose();
              });
          }
        });
    }
  }

  addMemberToList = () => {
    const {
      newMember, newMembers, groupOwner, groupMembers,
    } = this.state;
    if (newMember.length < 1) {
      return;
    }
    if (newMember === groupOwner) {
      sweetAlert('Info', 'Cannot add yourself. You are already part of the group.', 'warning');
      return;
    }

    if (groupMembers.includes(newMember) || newMembers.includes(newMember)) {
      sweetAlert('Info', `${newMember} already exists in the list.`, 'warning');
      return;
    }

    newMembers.push(newMember);
    this.setState({
      newMembers,
      newMember: '',
    });
  }

  handleDropboxChange = (e, { value }) => {
    this.setState({ newMember: value });
  }

  deleteFunction = (member) => {
    const { groupMembers, newMembers, deletedMembers } = this.state;

    if (groupMembers.includes(member)) {
      deletedMembers.push(member);
      this.setState({
        groupMembers: groupMembers.filter(m => m !== member),
        deletedMembers,
      });
    } else if (newMembers.includes(member)) {
      this.setState({ newMembers: newMembers.filter(m => m !== member) });
    }
  }

  renderMembersList = () => {
    const { groupMembers, newMembers, groupOwner } = this.state;
    const list = groupMembers.concat(newMembers);
    let content = (
      <List divided>
        {
          list.filter(w => w !== groupOwner).map(
            m => (
              <MemberRowItem
                // eslint-disable-next-line react/no-array-index-key
                key={m}
                selectedMember={m}
                deleteFunction={this.deleteFunction}
              />
            ),
          )}
      </List>
    );

    if (groupMembers.length === 0 && newMembers.length === 0) {
      content = (<Message visible>There is currently no members except you.</Message>);
    }
    return content;
  }

  render() {
    const { onClose, show, selectedGroup } = this.props;
    const {
      groupName, groupOwner, stateOptions,
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
              {groupOwner}
            </h3>
            <h3>Members:</h3>
            <FormField>
              <Dropdown
                placeholder="New member"
                search
                selection
                options={stateOptions}
                onChange={this.handleDropboxChange}
              />
              <Button onClick={this.addMemberToList}>Add member</Button>
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
};

GroupsModal.defaultProps = {
  selectedGroup: null,
};


export default GroupsModal;
