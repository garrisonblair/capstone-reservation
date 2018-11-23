import React, { Component } from 'react';
import { Button, Icon, Table, TableBody } from 'semantic-ui-react';
import api from '../../utils/api';
import GroupsRowItem from './GroupsRowItem';
import GroupsModal from './GroupsModal';
import './Groups.scss';


class Groups extends Component {
  state = {
    showModal: false,
    groups: [
      { id: 1, name: 'grpu1', members: [{ name: 'm1' }] }
    ],
  }

  syncGroups = () => {
    api.getMyGroups()
      .then((r) => {
        this.setState({ groups: r.data });
      });
  }

  showGroupsModal = () =>{this.setState({showModal: true})}

  closeGroupsModal = () =>{
    this.syncGroups();
    this.setState({showModal: false});
  }

  render() {
    const { groups, showModal } = this.state;
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
              <Table.HeaderCell textAlign="center">Name</Table.HeaderCell>
              <Table.HeaderCell> </Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <TableBody>
            {groups.map(
              g =>
                (<GroupsRowItem
                  key={g.id}
                  group={g}
                />)
            )}
          </TableBody>
        </Table>
        {showModal ? <GroupsModal onClose = {this.closeGroupsModal} /> : ''}
      </div>
    );
  }
}

export default Groups;
