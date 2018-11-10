import React, {Component} from 'react';
import AdminRequired from '../../HOC/AdminRequired';
import SideNav from '../SideNav';
import '../Admin.scss';


class Stats extends Component {
  render() {
    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={'stats'}/>
          <div className="admin__content">
            <div>Stats Content</div>
          </div>
        </div>
      </div>
    )
  }
}

export default AdminRequired(Stats);
