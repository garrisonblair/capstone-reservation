import React, { Component } from 'react';
import { Table, Button } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './GroupPrivilegeRequest.scss';

class PrivilegeRequestRow extends Component {
  handleDeny = () => {
    const { request } = this.props;
    sweetAlert({
      title: 'Warning',
      text: `Are you sure you want to deny privilege to group ${request.group}? Enter a reason.`,
      type: 'warning',
      input: 'text',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      confirmButtonText: 'Deny',
    }).then((r) => {
      if (r.value) {
        api.denyPrivilegeRequest(request.id, r.value)
          .then((r2) => {
            if (r2.status === 200) {
              sweetAlert('Success', 'It was successfully denied', 'success');
            }
          });
      }
    });
  }

  handleApprove = () => {
    const { request } = this.props;
    api.approvePrivilegeRequest(request.id)
      .then((r) => {
        console.log(r);
      });
  }

  render() {
    const { request } = this.props;
    console.log(request);
    return (
      <Table.Row>
        <Table.Cell>
          {request.group}
        </Table.Cell>
        <Table.Cell>
          {request.privilege_category}
        </Table.Cell>
        <Table.Cell>
          {request.status}
        </Table.Cell>
        <Table.Cell>
          <Button color="blue" onClick={this.handleApprove}>Accept</Button>
        </Table.Cell>
        <Table.Cell>
          <Button color="red" onClick={this.handleDeny}>Deny</Button>
        </Table.Cell>
      </Table.Row>
    );
  }
}

PrivilegeRequestRow.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  request: PropTypes.object.isRequired,
};

export default PrivilegeRequestRow;
