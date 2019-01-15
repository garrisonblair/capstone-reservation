import React, { Component } from 'react';
import { Button, Dropdown } from 'semantic-ui-react';

class RequestPrivilege extends Component {
  status = {
    privileges: [],
    options: [{ value: 1, text: 'no' }],
    dropdownValue: '',
  }

  handleRequestPrivilege = () => {

  }

  handlePrivilegeChange = (e, v) => {
    console.log(v);
  }

  render() {
    const { options, dropdownValue } = this.status;
    return (
      <div>
        <h3>Privilege</h3>
        <Dropdown
          placeholder="Privileges"
          options={options}
          selection
          value={dropdownValue}
          onChange={this.handlePrivilegeChange}
        />
        <Button color="blue" onClick={this.handleRequestPrivilege}>Request privilege</Button>
      </div>
    );
  }
}


export default RequestPrivilege;
