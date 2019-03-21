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
    if (myUserId === group.owner.id) {
      label = <Label color="yellow">OWNER</Label>;
    }
    return label;
  }

  render() {
    const {
      group,
      syncGroupsList,
      myUserId,
      syncPrivileges,
    } = this.props;
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
              syncPrivileges={syncPrivileges}
              isAdmin={myUserId === group.owner.id}
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
    owner: PropTypes.object.isRequired,
    privilege_category: PropTypes.number,
  }).isRequired,
  myUserId: PropTypes.number.isRequired,
  syncPrivileges: PropTypes.func,
};

GroupsRowItem.defaultProps = {
  syncPrivileges: null,
};

export default GroupsRowItem;
