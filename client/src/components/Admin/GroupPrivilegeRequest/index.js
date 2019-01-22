import React, { Component } from 'react';
import { Table } from 'semantic-ui-react';
import api from '../../../utils/api';
import PrivilegeRequestRow from './PrivilegeRequestRow';
import './GroupPrivilegeRequest.scss';


class GroupPrivilegeRequest extends Component {
  state = {
    requests: [],
  }

  componentDidMount() {
    api.getPrivilegeRequests()
      .then((r) => {
        if (r.status === 200) {
          this.setState({ requests: r.data });
        }
      });
  }

  render() {
    const { requests } = this.state;
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
                Status
              </Table.HeaderCell>
              {/* This tab is for approved buttons */}
              <Table.HeaderCell />
              {/* This tab is for denied buttons */}
              <Table.HeaderCell />
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {requests.map(r => <PrivilegeRequestRow request={r} key={r.id} />)}
          </Table.Body>
        </Table>
      </div>
    );
  }
}

export default GroupPrivilegeRequest;
