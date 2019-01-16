import React, { Component } from 'react';
import { Table } from 'semantic-ui-react';
import PropTypes from 'prop-types';
// import api from '../../../utils/api';
import './GroupPrivilegeRequest.scss';

class PrivilegeRequestRow extends Component {
  handleDeny = () => {

  }

  handleApprove = () => {

  }

  render() {
    const { group } = this.props;
    console.log(group);
    return (
      <Table.Row>
        <Table.Cell>
          {group.name}
        </Table.Cell>
        <Table.Cell>
          {group.name}
        </Table.Cell>
      </Table.Row>
    );
  }
}

PrivilegeRequestRow.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  group: PropTypes.object.isRequired,
};

export default PrivilegeRequestRow;
