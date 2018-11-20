import React, {Component} from 'react';
import AdminRequired from '../HOC/AdminRequired';
import PropTypes from 'prop-types';
import {withRouter} from 'react-router-dom';
import SideNav from './SideNav';
import './Admin.scss';


class Admin extends Component {

  componentDidMount = () => {
    document.title = 'Capstone Settings'
  }
  goToSettings = () => {
    this.props.history.push('/admin/settings')
  }

  goToPrivileges = () => {
    this.props.history.push('/admin/privileges')
  }

  goToRooms = () => {
    this.props.history.push('/admin/rooms')
  }

  goToStats = () => {
    this.props.history.push('/admin/stats')
  }

  render() {
    let {content, menuType} = this.props;
    const navConfig=[
      {text:'Settings', menu:'settings', function:this.goToSettings},
      {text:'Privileges', menu:'privileges', function:this.goToPrivileges},
      {text:'Rooms', menu:'rooms', function:this.goToRooms},
      {text:'Stats', menu:'stats', function:this.goToStats},
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

export default withRouter(AdminRequired(Admin));
