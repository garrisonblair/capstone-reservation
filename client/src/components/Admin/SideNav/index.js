import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';
import './SideNav.scss';


class SideNav extends Component {
  renderNavItem = () => {
    // eslint-disable-next-line react/prop-types
    const { selectedMenu, navConfig, history } = this.props;
    return (
      <ul>
        {navConfig.map(row => (
          <li
            className={selectedMenu === row.menu ? 'active' : ''}
            onClick={() => { history.push(row.path); }}
            key={row.menu}
            onKeyDown={() => {}}
          >
            {row.text}
          </li>))}
      </ul>
    );
  }

  render() {
    return (
      <div className="sidenav">
        {this.renderNavItem()}
      </div>
    );
  }
}

SideNav.propTypes = {
  selectedMenu: PropTypes.string.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  navConfig: PropTypes.array,
};

SideNav.defaultProps = {
  navConfig: [
    { text: 'Calendar', menu: 'calendar', path: '/' },
    { text: 'Settings', menu: 'settings', path: '/admin/settings' },
    { text: 'Privileges', menu: 'privileges', path: '/admin/privileges' },
    { text: 'Rooms', menu: 'rooms', path: '/admin/rooms' },
    { text: 'Stats', menu: 'stats', path: '/admin/stats' },
    { text: 'Bookers', menu: 'bookers', path: '/admin/bookers' },
    { text: "Group's Privilege Request", menu: 'group-privilege-request', path: '/admin/privilegeRequest' },
  ],
};

export default withRouter(SideNav);
