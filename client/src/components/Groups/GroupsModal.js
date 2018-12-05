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
    // eslint-disable-next-line react/no-unused-state
    groupId: '',
    // eslint-disable-next-line react/no-unused-state
    groupOwner: '',
    groupName: '',
    groupMembers: [],
    newMember: '',
  }

  componentDidMount() {
    const { selectedGroup } = this.props;
    if (selectedGroup != null) {
      this.setState({
        // eslint-disable-next-line react/no-unused-state
        groupId: selectedGroup.id,
        groupOwner: selectedGroup.owner,
        groupName: selectedGroup.name,
        groupMembers: selectedGroup.members,
      });
    } else {
      this.setState({
        groupMembers: ['27129312'],
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
    const { groupName, groupMembers } = this.state;
    const { onClose } = this.props;
    if (!this.verifyModalForm()) {
      return;
    }
    api.createGroup(groupName, groupMembers)
      .then((r) => {
        if (r.status === 201) {
          sweetAlert('Completed', 'A group was created.', 'success')
            .then(() => {
              onClose();
            });
        }
      });
  }

  addMemberToList = () => {
    const { groupMembers, newMember } = this.state;
    if (newMember.length < 1) {
      return;
    }
    console.log(newMember);
    groupMembers.push(newMember);
    this.setState({
      groupMembers,
      newMember: '',
    });
  }

  handleAddMemberOnChange = (e) => {
    this.setState({ newMember: e.target.value });
  }

  renderMembersList = () => {
    let { groupMembers } = this.state;
    groupMembers = groupMembers.slice(1, groupMembers.length);
    let content = '';
    if (groupMembers.length !== 0) {
      content = (
        <List divided>
          {
            groupMembers.map(
              (m, index) => (
                <MemberRowItem
                  // eslint-disable-next-line react/no-array-index-key
                  key={index}
                  selectedMember={m}
                />
              ),
            )}
        </List>
      );
    } else {
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
    privilege_category: PropTypes.number.isRequired,
    members: PropTypes.array.isRequired,
  }),
};

GroupsModal.defaultProps = {
  selectedGroup: null,
};


export default GroupsModal;
