import React, { Component } from 'react';
import {
  Button, Icon, Table, TableBody,
} from 'semantic-ui-react';
import api from '../../utils/api';
import GroupsRowItem from './GroupsRowItem';
import GroupsModal from './GroupsModal';
import './Groups.scss';


class Groups extends Component {
  state = {
    showModal: false,
    groups: [],
    myUserId: 0,
  }

  componentDidMount() {
    this.syncGroups();
    api.getMyUser()
      .then((r) => {
        if (r.status === 200) {
          this.setState({ myUserId: r.data.id });
        }
      });
  }

  syncGroups = () => {
    api.getMyGroups()
      .then((r) => {
        this.setState({ groups: r.data });
      });
  }

  showGroupsModal = () => { this.setState({ showModal: true }); }

  closeGroupsModal = () => {
    this.syncGroups();
    this.setState({ showModal: false });
  }

  render() {
    const { groups, showModal, myUserId } = this.state;
    return (
      <div id="groups">
        <h1>Groups</h1>
        <Button icon labelPosition="left" primary size="small" onClick={this.showGroupsModal}>
          <Icon name="plus" />
          Add
        </Button>
        <Table>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Name</Table.HeaderCell>
              <Table.HeaderCell>Privilege</Table.HeaderCell>
              <Table.HeaderCell> </Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <TableBody>
            {groups.map(
              g => (
                <GroupsRowItem
                  key={g.id}
                  group={g}
                  syncGroupsList={this.syncGroups}
                  myUserId={myUserId}
                />
              ),
            )}
          </TableBody>
        </Table>
        {showModal ? <GroupsModal show onClose={this.closeGroupsModal} isAdmin /> : ''}
      </div>
    );
  }
}

export default Groups;