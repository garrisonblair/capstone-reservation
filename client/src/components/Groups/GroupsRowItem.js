import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button, Table, Label } from 'semantic-ui-react';
import api from '../../utils/api';
import GroupsModal from './GroupsModal';
// import sweetAlert from 'sweetalert2';


class GroupsRowItem extends Component {
  state = {
    openModal: false,
    me: '',
  }

  componentDidMount() {
    // eslint-disable-next-line react/destructuring-assignment
    api.getMyUser()
      .then((r) => {
        this.setState({ me: r.data.id });
      });
  }

  openModal = () => {
    this.setState({ openModal: true });
  }

  closeModal = () => {
    const { syncGroupsList } = this.props;
    syncGroupsList();
    this.setState({ openModal: false });
  }


  render() {
    const { group, syncGroupsList } = this.props;
    const { openModal, me } = this.state;
    return (
      <Table.Row key={group.id}>
        <Table.Cell>
          <h4>{group.name}</h4>
        </Table.Cell>
        <Table.Cell>
          {group.owner === me ? <Label color="yellow">ADMIN</Label> : <Label color="grey">MEMBER</Label>}
        </Table.Cell>
        <Table.Cell textAlign="center">
          <Button icon="edit" onClick={this.openModal} />
        </Table.Cell>
        {openModal ? (
          <GroupsModal
            show
            selectedGroup={group}
            onClose={this.closeModal}
            syncGroupsList={syncGroupsList}
          />
        ) : ''}
      </Table.Row>
    );
  }
}

GroupsRowItem.propTypes = {
  syncGroupsList: PropTypes.func.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  group: PropTypes.object.isRequired,
};

export default GroupsRowItem;
