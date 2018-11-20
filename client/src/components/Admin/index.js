import React, {Component} from 'react';
import AdminRequired from '../HOC/AdminRequired';
import PropTypes from 'prop-types';
import SideNav from '../SideNav';
import './Admin.scss';


class Admin extends Component {

  componentDidMount = () => {
    document.title = 'Capstone Settings'
  }

  render() {
    let {content, menuType} = this.props;
    const navConfig=[
      {text:'Settings', menu:'settings', path:'/admin/settings'},
      {text:'Privileges', menu:'privileges', path:'/admin/privileges'},
      {text:'Rooms', menu:'rooms', path:'/admin/rooms'},
      {text:'Stats', menu:'stats', path:'/admin/stats'}
    ];
    return (
      <div className="admin">
        <div className="admin__wrapper">
          <SideNav selectedMenu={menuType} navConfig={navConfig}/>
          <div className="admin__content">
          {content}
          </div>
        </div>
      </div>
    )
  }
}

Admin.propTypes = {
  menuType: PropTypes.string.isRequired,
  content: PropTypes.object.isRequired
}

export default AdminRequired(Admin);
