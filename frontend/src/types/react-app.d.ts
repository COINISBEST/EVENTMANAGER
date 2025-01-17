/// <reference types="react" />
/// <reference types="react-dom" />

declare namespace React {
  interface Component<P = {}, S = {}, SS = any> extends ComponentLifecycle<P, S, SS> {}
  
  interface ComponentClass<P = {}, S = ComponentState> extends StaticLifecycle<P, S> {
    new (props: P, context?: any): Component<P, S>;
    propTypes?: WeakValidationMap<P> | undefined;
    contextType?: Context<any> | undefined;
    contextTypes?: ValidationMap<any> | undefined;
    childContextTypes?: ValidationMap<any> | undefined;
    defaultProps?: Partial<P> | undefined;
    displayName?: string | undefined;
  }

  interface ErrorInfo {
    componentStack: string;
  }

  interface ComponentLifecycle<P, S, SS = any> {
    componentDidMount?(): void;
    componentDidUpdate?(prevProps: Readonly<P>, prevState: Readonly<S>, snapshot?: SS): void;
    componentWillUnmount?(): void;
    componentDidCatch?(error: Error, errorInfo: ErrorInfo): void;
    getDerivedStateFromError?(error: any): Partial<S> | null;
    getDerivedStateFromProps?(props: Readonly<P>, state: S): Partial<S> | null;
    getSnapshotBeforeUpdate?(prevProps: Readonly<P>, prevState: Readonly<S>): SS | null;
  }
}

declare module "*.svg" {
  const content: any;
  export default content;
}

declare module "*.png" {
  const content: any;
  export default content;
}

declare module "*.jpg" {
  const content: any;
  export default content;
} 