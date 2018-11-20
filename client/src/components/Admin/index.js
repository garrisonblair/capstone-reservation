import React, {Component} from 'react';
import AdminRequired from '../HOC/AdminRequired';
import SideNav from './SideNav';
import Settings from './Settings';
import './Admin.scss';


class Admin extends Component {

  componentDidMount = () => {
    document.title = 'Capstone Settings'
  }

  render() {
    let {content, menuType} = this.props;
    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={menuType}/>
          <div className="admin__content">
          {content}
          </div>
        </div>
      </div>
    )
  }
}

export default AdminRequired(Admin);
