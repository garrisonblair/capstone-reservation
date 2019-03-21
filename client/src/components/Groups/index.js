import React, { Component } from 'react';
import PropTypes from 'prop-types';
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
    const { syncPrivileges } = this.props;
    api.getMyGroups()
      .then((r) => {
        this.setState({ groups: r.data, isLoading: false });
      });
    syncPrivileges();
  }

  showGroupsModal = () => { this.setState({ showModal: true }); }

  closeGroupsModal = () => {
    this.syncGroups();
    this.setState({ showModal: false });
  }

  render() {
    const { showTitle, syncPrivileges } = this.props;
    const {
      groups, showModal, myUserId, isLoading,
    } = this.state;
    return (
      <div id="groups">
        { showTitle ? <h1>Groups</h1> : null }
        <Segment loading={isLoading}>
          <Button icon labelPosition="left" primary size="small" onClick={this.showGroupsModal}>
            <Icon name="plus" />
            Add
          </Button>
          <Table unstackable>
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
                    syncPrivileges={syncPrivileges}
                    syncGroupsList={this.syncGroups}
                    myUserId={myUserId}
                  />
                ),
              )}
            </TableBody>
          </Table>
          {showModal ? <GroupsModal show syncPrivileges={syncPrivileges} onClose={this.closeGroupsModal} isAdmin /> : ''}
        </Segment>
      </div>
    );
  }
}

Groups.propTypes = {
  showTitle: PropTypes.bool,
  syncPrivileges: PropTypes.func,
};

Groups.defaultProps = {
  showTitle: false,
  syncPrivileges: null,
};

export default Groups;
