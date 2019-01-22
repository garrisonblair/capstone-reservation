import React, { Component } from 'react';
import { Table, Button } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './GroupPrivilegeRequest.scss';

class PrivilegeRequestRow extends Component {
  handleDeny = () => {
    const { request, syncMethod } = this.props;
    sweetAlert({
      title: 'Warning',
      html: `Are you sure you want to deny privilege to group ${request.group.name}? <br />Enter a reason.`,
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
              syncMethod();
            }
          });
      }
    });
  }

  handleApprove = () => {
    const { request, syncMethod } = this.props;
    api.approvePrivilegeRequest(request.id)
      .then((r) => {
        if (r.status === 200) {
          sweetAlert('Success', 'It was successfully approved', 'success');
          syncMethod();
        }
      });
  }

  renderButtons = () => (
    <div>
      <Button color="blue" onClick={this.handleApprove}>Accept</Button>
      <Button color="red" onClick={this.handleDeny}>Deny</Button>
    </div>
  )

  render() {
    const { request } = this.props;
    return (
      <Table.Row>
        <Table.Cell>
          {request.group.name}
        </Table.Cell>
        <Table.Cell>
          {request.privilege_category.name}
        </Table.Cell>
        <Table.Cell>
          {request.status}
        </Table.Cell>
        <Table.Cell>
          {request.status === 'Pending' ? this.renderButtons() : null}
        </Table.Cell>
      </Table.Row>
    );
  }
}

PrivilegeRequestRow.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  request: PropTypes.object.isRequired,
  syncMethod: PropTypes.func.isRequired,
};

export default PrivilegeRequestRow;
