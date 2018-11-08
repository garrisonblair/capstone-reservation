import React, {Component} from 'react';
import api from '../../utils/api';
import AdminRequired from '../HOC/AdminRequired';
import SideNav from './SideNav';
import './Admin.scss';


class PrivilegeCategory extends Component {

  getPrivileges() {
    api.getPrivileges()
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      console.log(error);
    })
  }

  componentDidMount() {
    this.getPrivileges();
  }

  render() {
    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={'privileges'}/>
          <div className="admin__content">
            <div>Privileges</div>
          </div>
        </div>
      </div>
    )
  }
}

export default AdminRequired(PrivilegeCategory);
