import React, { Component } from 'react';
import {
  Button, Icon, Table, TableBody, Segment,
} from 'semantic-ui-react';
import api from '../../utils/api';
import storage from '../../utils/local-storage';
import GroupsRowItem from './GroupsRowItem';
import GroupsModal from './GroupsModal';
import './Groups.scss';


class Groups extends Component {
  state = {
    showModal: false,
    groups: [],
    myUserId: 0,
    isLoading: false,
  }

  componentDidMount() {
    this.syncGroups();
    api.getUser(storage.getUser().id)
      .then((r) => {
        if (r.status === 200) {
          this.setState({ myUserId: r.data.id });
        }
      });
  }

  syncGroups = () => {
    this.setState({ isLoading: true });
    api.getMyGroups()
      .then((r) => {
        this.setState({ groups: r.data, isLoading: false });
      });
  }

  showGroupsModal = () => { this.setState({ showModal: true }); }

  closeGroupsModal = () => {
    this.syncGroups();
    this.setState({ showModal: false });
  }

  render() {
    const {
      groups, showModal, myUserId, isLoading,
    } = this.state;
    return (
      <div id="groups">
        <h1>Groups</h1>
        <Segment loading={isLoading}>
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
        </Segment>
      </div>
    );
  }
}

export default Groups;
