import React, { Component } from 'react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import {
  Modal, Button, FormField, Input, List, Message,
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
    newMember: '',
  }

  componentDidMount() {
    const { selectedGroup } = this.props;
    if (selectedGroup !== null) {
      this.setState({
        groupId: selectedGroup.id,
        groupOwner: selectedGroup.owner,
        groupName: selectedGroup.name,
        groupMembers: selectedGroup.members,
      });
    } else {
      this.setState({
        newMembers: ['27129312'],
        groupOwner: '27129312',
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
    const { newMember, newMembers } = this.state;
    if (newMember.length < 1) {
      return;
    }
    newMembers.push(newMember);
    this.setState({
      newMembers,
      newMember: '',
    });
  }

  handleAddMemberOnChange = (e) => {
    this.setState({ newMember: e.target.value });
  }

  renderMembersList = () => {
    const { groupMembers, newMembers, groupOwner } = this.state;
    let content = '';
    content = (
      <List divided>
        {
          groupMembers.filter(w => w !== groupOwner).map(
            (m, index) => (
              <MemberRowItem
                // eslint-disable-next-line react/no-array-index-key
                key={index}
                selectedMember={m}
              />
            ),
          )}
        {
          newMembers.filter(w => w !== groupOwner).map(
            (m, index) => (
              <MemberRowItem
                // eslint-disable-next-line react/no-array-index-key
                key={index + 3}
                selectedMember={m}
              />
            ),
          )
        }
      </List>
    );
    if (groupMembers.length === 0 && newMembers.length === 0) {
      content = (<Message visible>There is currently no members except you.</Message>);
    }
    return content;
  }

  render() {
    const { onClose, show, selectedGroup } = this.props;
    const { groupName, newMember, groupOwner } = this.state;
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
              <Input
                size="small"
                action={<Button content="Add" onClick={this.addMemberToList} />}
                onChange={this.handleAddMemberOnChange}
                placeholder="Add members"
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

GroupsModal.propTypes = {
  onClose: PropTypes.func.isRequired,
  show: PropTypes.bool.isRequired,
  selectedGroup: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    is_verified: PropTypes.bool.isRequired,
    owner: PropTypes.string.isRequired,
    privilege_category: PropTypes.number,
    members: PropTypes.array.isRequired,
  }),
};

GroupsModal.defaultProps = {
  selectedGroup: null,
};


export default GroupsModal;
