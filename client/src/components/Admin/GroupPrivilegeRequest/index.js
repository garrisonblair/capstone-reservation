import React, { Component } from 'react';
import { Table } from 'semantic-ui-react';
import api from '../../../utils/api';
import PrivilegeRequestRow from './PrivilegeRequestRow';
import './GroupPrivilegeRequest.scss';


class GroupPrivilegeRequest extends Component {
  state = {
    groups: [],
  }

  componentDidMount() {
    api.getMyGroups()
      .then((r) => {
        if (r.status === 200) {
          this.setState({ groups: r.data });
        }
      });
  }

  render() {
    const { groups } = this.state;
    return (
      <div id="group-privilege-request">
        <h2>Group&lsquo;s Privilege Request</h2>
        <Table>
          <Table.Header>
            <Table.Row key="1">
              <Table.HeaderCell>
                Group&lsquo;s name
              </Table.HeaderCell>
              <Table.HeaderCell>
                Requested Privilege
              </Table.HeaderCell>
              <Table.HeaderCell>
                {/* This tab is for accept buttons */}
              </Table.HeaderCell>
              <Table.HeaderCell>
                {/* This tab is for denied buttons */}
              </Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {groups.map(g => <PrivilegeRequestRow group={g} key={g.id} />)}
          </Table.Body>
        </Table>
      </div>
    );
  }
}

export default GroupPrivilegeRequest;
