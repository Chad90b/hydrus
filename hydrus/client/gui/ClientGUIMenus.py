from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG

from hydrus.core import HydrusConstants as HC
from hydrus.core import HydrusData
from hydrus.core import HydrusGlobals as HG
from hydrus.core import HydrusText
from hydrus.client.gui import QtPorting as QP

def AppendMenu( menu, submenu, label ):
    
    label = SanitiseLabel( label )
    
    submenu.setTitle( label )
    menu.addMenu( submenu )
    
def AppendMenuBitmapItem( menu, label, description, bitmap, callable, *args, **kwargs ):
    
    label = SanitiseLabel( label )
    
    menu_item = QW.QAction( menu )
    
    if HC.PLATFORM_MACOS:
        
        menu_item.setMenuRole( QW.QAction.ApplicationSpecificRole )
        
    
    menu_item.setText( HydrusText.ElideText( label, 128, elide_center = True ) )
    
    menu_item.setStatusTip( description )
    menu_item.setToolTip( description )
    menu_item.setWhatsThis( description )
    
    menu_item.setIcon( QG.QIcon( bitmap ) )
    
    menu.addAction(menu_item)
    
    BindMenuItem( menu_item, callable, *args, **kwargs )
    
    return menu_item
    
def AppendMenuCheckItem( menu, label, description, initial_value, callable, *args, **kwargs ):
    
    label = SanitiseLabel( label )
    
    menu_item = QW.QAction( menu )
    
    if HC.PLATFORM_MACOS:
        
        menu_item.setMenuRole( QW.QAction.ApplicationSpecificRole )
        
    
    menu_item.setText( HydrusText.ElideText( label, 128, elide_center = True ) )
    
    menu_item.setStatusTip( description )
    menu_item.setToolTip( description )
    menu_item.setWhatsThis( description )
    
    menu_item.setCheckable( True )
    menu_item.setChecked( initial_value )
    
    menu.addAction( menu_item )
    
    BindMenuItem( menu_item, callable, *args, **kwargs )
    
    return menu_item
    
def AppendMenuItem( menu, label, description, callable, *args, **kwargs ):
    
    label = SanitiseLabel( label )
    
    menu_item = QW.QAction( menu )
    
    if HC.PLATFORM_MACOS:
        
        menu_item.setMenuRole( QW.QAction.ApplicationSpecificRole )
        
    
    elided_label = HydrusText.ElideText( label, 128, elide_center = True )
    
    menu_item.setText( elided_label )
    
    if elided_label != label:
        
        menu_item.setToolTip( label )
        
    else:
        
        menu_item.setToolTip( description )
        
    
    menu_item.setStatusTip( description )
    menu_item.setWhatsThis( description )

    menu.addAction( menu_item )
    
    BindMenuItem( menu_item, callable, *args, **kwargs )
    
    return menu_item
    
def AppendMenuLabel( menu, label, description = '' ):
    
    if description is None:
        
        description = ''
        
    
    menu_item = QW.QAction( menu )

    if HC.PLATFORM_MACOS:
        
        menu_item.setMenuRole( QW.QAction.ApplicationSpecificRole )
        
    
    menu_item.setText( HydrusText.ElideText( label, 128, elide_center = True ) )
    
    menu_item.setStatusTip( description )
    menu_item.setToolTip( description )
    menu_item.setWhatsThis( description )

    menu.addAction( menu_item )
    
    BindMenuItem( menu_item, HG.client_controller.pub, 'clipboard', 'text', label )
    
    return menu_item
    
def AppendSeparator( menu ):
    
    num_items = len( menu.actions() )
    
    if num_items > 0:
        
        last_item = menu.actions()[-1]
        
        if not last_item.isSeparator():
            
            menu.addSeparator()
            
        
    
def BindMenuItem( menu_item, callable, *args, **kwargs ):
    
    event_callable = GetEventCallable( callable, *args, **kwargs )
    
    menu_item.triggered.connect( event_callable )
    
def DestroyMenu( menu ):
    
    if menu is None:
        
        return
        
    
    if QP.isValid( menu ):
        
        menu.deleteLater()
        
    
def GetEventCallable( callable, *args, **kwargs ):
    
    def event_callable( checked_state ):
        
        if HG.menu_profile_mode:
            
            summary = 'Profiling menu: ' + repr( callable )
            
            HydrusData.ShowText( summary )
            
            HydrusData.Profile( summary, 'callable( *args, **kwargs )', globals(), locals() )
            
        else:
            
            callable( *args, **kwargs )
            
        
    
    return event_callable
    
def SanitiseLabel( label ):
    
    if label == '':
        
        label = '-invalid label-'
        
    
    return label.replace( '&', '&&' )
    
