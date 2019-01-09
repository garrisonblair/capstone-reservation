import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button, Table, Label } from 'semantic-ui-react';
import GroupsModal from './GroupsModal';


class GroupsRowItem extends Component {
  state = {
    openModal: false,
  }

  openModal = () => {
    this.setState({ openModal: true });
  }

  closeModal = () => {
    const { syncGroupsList } = this.props;
    syncGroupsList();
    this.setState({ openModal: false });
  }

  renderPrivilege = () => {
    const { group, myUserId } = this.props;
    let label = <Label color="grey">MEMBER</Label>;
    if (myUserId === group.owner.user.id) {
      label = <Label color="yellow">ADMIN</Label>;
    }
    return label;
  }

  render() {
    const { group, syncGroupsList, myUserId } = this.props;
    const { openModal } = this.state;
    return (
      <Table.Row key={group.id}>
        <Table.Cell>
          <h4>{group.name}</h4>
        </Table.Cell>
        <Table.Cell>
          {this.renderPrivilege()}
        </Table.Cell>
        <Table.Cell textAlign="center">
          <Button icon="edit" onClick={this.openModal} />
          {openModal ? (
            <GroupsModal
              show
              selectedGroup={group}
              onClose={this.closeModal}
              syncGroupsList={syncGroupsList}
              isAdmin={myUserId === group.owner.user.id}
            />
          ) : ''}
        </Table.Cell>
      </Table.Row>
    );
  }
}

GroupsRowItem.propTypes = {
  syncGroupsList: PropTypes.func.isRequired,
  group: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    is_verified: PropTypes.bool.isRequired,
    owner: PropTypes.object.isRequired,
    privilege_category: PropTypes.number,
    members: PropTypes.array.isRequired,
  }).isRequired,
  myUserId: PropTypes.number.isRequired,
};

export default GroupsRowItem;
