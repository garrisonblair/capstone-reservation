import React, {Component} from 'react';
import AdminRequired from '../HOC/AdminRequired';
import SideNav from './SideNav';
import './Admin.scss';


class PrivilegeCategory extends Component {
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
